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