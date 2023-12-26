from django.shortcuts import render
from .models import AvailableRooms
from .serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .tasks import release_reserved_rooms
from rest_framework.response import Response
from rest_framework import status 
import stripe
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect

# Create your views here.
class BookingView(APIView):
    def post(self, request):
        # room_id = 68
        # tenant_id = 2
        # no_of_rooms = 1
        room_id = request.data.get('room_id')
        tenant_id = request.data.get('tenant_id')
        no_of_rooms = request.data.get('no_of_rooms')

        available_rooms = AvailableRooms.objects.get(room_id=room_id)

        if available_rooms.available_quantity < no_of_rooms:
            return Response({'error': 'Not enough rooms available'}, status=status.HTTP_400_BAD_REQUEST)
          
        # Reserve the rooms
        booking_data = {
            'room_id': room_id,
            'tenant_id': tenant_id,
            'status': 'reserved',
            'no_of_rooms': no_of_rooms,
        }

        booking_serializer = BookingSerializer(data=booking_data)

        if booking_serializer.is_valid():
            with transaction.atomic():
                booking = booking_serializer.save()

                available_rooms.available_quantity -= no_of_rooms
                available_rooms.save()

            # Schedule the task to release reserved rooms after 10 minutes
            release_reserved_rooms.apply_async((booking.id,), countdown=60)

            # Commit the transaction before initiating Stripe payment
            return self.initiate_stripe_payment(request, booking)

        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
        

    def initiate_stripe_payment(self, request, booking):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1ONZrJSEWXt1qBzUCZoGMgVE',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + f'/?success=true&session_id={booking.id}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            return Response({'checkout_url': checkout_session.url})

        except Exception as e:
            print(f"Error initiating Stripe payment: {e}")
            return Response({'error': 'Error initiating Stripe payment'}, status=500)

            # Log or handle the error as needed
            # Assuming you have a field in your Booking model to store the Stripe session ID
            # booking.stripe_session_id = checkout_session.id
            # booking.save()

stripe.api_key = settings.STRIPE_SECRET_KEY 

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1ONZrJSEWXt1qBzUCZoGMgVE',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {'error':'Something went wrong creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

# @csrf_exempt
# def my_webhook_view(request):
#   payload = request.body
#   event = None

#   try:
#     event = stripe.Event.construct_from(
#       json.loads(payload), stripe.api_key
#     )
#   except ValueError as e:
#     # Invalid payload
#     return HttpResponse(status=400)

#   # Handle the event
#   if event.type == 'payment_intent.succeeded':
#     payment_intent = event.data.object # contains a stripe.PaymentIntent
#     # Then define and call a method to handle the successful payment intent.
#     # handle_payment_intent_succeeded(payment_intent)
#   elif event.type == 'payment_method.attached':
#     payment_method = event.data.object # contains a stripe.PaymentMethod
#     # Then define and call a method to handle the successful attachment of a PaymentMethod.
#     # handle_payment_method_attached(payment_method)
#   # ... handle other event types
#   else:
#     print('Unhandled event type {}'.format(event.type))

#   return HttpResponse(status=200)