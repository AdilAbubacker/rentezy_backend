from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_rent_reminders, task_one, generate_recurring_payments
from .kafka_producers import kafka_producer
from django.conf import settings
from rest_framework.views import APIView
from .models import RentalAgreement, MonthlyPayment
from .serializers import RentalAgreementSerializer, MonthlyPaymentSerializer
from rest_framework.response import Response
from rest_framework import status 
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY 

# Create your views here.
def test(request):
    # generate_recurring_payments.delay()
    message = '{"user_id":"3","message":"hpw adfri"}'
    print(message)
    send_rent_reminders.delay()
    # kafka_producer.produce_message(message=message,topic=settings.KAFKA_NOTIFICATIONS_TOPIC)
    return HttpResponse("Hello, this is a response.")

class RentedPropertiesListView(APIView):
    def get(self, request):
        bookings = RentalAgreement.objects.all()
        serializer = RentalAgreementSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class RentPaymentDeatailsView(APIView):
    def get(self, request, rent_id):
        agreement = RentalAgreement.objects.get(id=rent_id)
        payments = MonthlyPayment.objects.filter(rental_agreement=agreement)
          
        # Serialize RentalAgreement along with MonthlyPayments
        agreement_serializer = RentalAgreementSerializer(agreement)
        payments_serializer = MonthlyPaymentSerializer(payments, many=True)

        # Combine the serialized data
        data = {
            'rental_agreement': agreement_serializer.data,
            'monthly_payments': payments_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    

class RentPaymentView(APIView):
    def post(self, request):
        monthly_payment_id = request.data.get('monthly_payment_id')
        monthly_payment = MonthlyPayment.objects.get(id=monthly_payment_id)
        total_price = monthly_payment.amount + monthly_payment.fine
        # initiating Stripe payment
        try:
            price = int(total_price)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount':  int(price * 100), 
                            'product_data': {
                                'name': monthly_payment.id,
                                'images':['https://images.pexels.com/photos/3769739/pexels-photo-3769739.jpeg'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata = {
                    'rent_id':monthly_payment.id,
                    'amount': price,
                },
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/my-properties/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            return Response({'checkout_url': checkout_session.url},status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error initiating Stripe payment: {e}")
            return Response({'error': 'Error initiating Stripe payment'}, status=500)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    print('Payload:', payload)
    print('Signature Header:', sig_header)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print('Error parsing payload: {}'.format(str(e)))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Error verifying webhook signature: {}'.format(str(e)))
        return HttpResponse(status=400)

    # Change the booking status to reserved on checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        charge_id = session['payment_intent']
        print('Charge ID:', charge_id)

        rent_id = session['metadata']['rent_id']
        payment = MonthlyPayment.objects.get(pk=rent_id)
        payment.is_paid = True
        payment.paid_on = timezone.now().date()
        payment.save()

    return HttpResponse(status=200)