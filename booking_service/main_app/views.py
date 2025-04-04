from django.http import HttpResponse
from django.shortcuts import render
from .models import AvailableRooms, Booking
from .serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .tasks import release_reserved_rooms
from rest_framework.response import Response
from rest_framework import status 
import stripe
from datetime import datetime 
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY 

# Create your views here.
class BookingView(APIView):
    def post(self, request):
        room_id = request.data.get('room_id')
        tenant_id = request.data.get('tenant_id')
        no_of_rooms = request.data.get('no_of_rooms')
        move_in_date_str = request.data.get('move_in_date')

        # Parse MUI-formatted date to Python datetime
        move_in_date = datetime.strptime(move_in_date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()

        available_rooms = AvailableRooms.objects.get(room_id=room_id)

        if int(available_rooms.available_quantity) < int(no_of_rooms):
            return Response({'error': 'Not enough rooms available'}, status=status.HTTP_400_BAD_REQUEST)
          
        # Reserve the rooms
        booking_data = {
            'room_id': room_id,
            'tenant_id': tenant_id,
            'status': 'reserved',
            'no_of_rooms': no_of_rooms,
            'move_in_date': move_in_date
        }

        booking_serializer = BookingSerializer(data=booking_data)

        if booking_serializer.is_valid():
            try:
                with transaction.atomic():
                    # Re-fetch within transaction to get the most up-to-date data
                    available_rooms = AvailableRooms.objects.get(room_id=room_id)


                    # Deduct the rooms and save; this should trigger the constraint if it goes negative
                    available_rooms.available_quantity -= no_of_rooms
                    available_rooms.save()
                    
                    booking = booking_serializer.save()

            except IntegrityError:
                return Response({'error': 'Not enough rooms available'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Schedule the task to release reserved rooms after 10 minutes
            release_reserved_rooms.apply_async((booking.id,), countdown=300)
            
            # initiating Stripe payment
            try:
                price = int(available_rooms.price)
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'inr',
                                'unit_amount':  int(price * 100), 
                                'product_data': {
                                    'name': booking.id,
                                    'images':['https://images.pexels.com/photos/3769739/pexels-photo-3769739.jpeg'],
                                },
                            },
                            'quantity': 1,
                        },
                    ],
                    metadata = {
                        'booking_id':booking.id,
                        'amount': price,
                    },
                    payment_method_types=['card'],
                    mode='payment',
                    success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=settings.SITE_URL + '/?canceled=true',
                )
                booking.stripe_session_id = checkout_session.id
                booking.save()
                return Response({'checkout_url': checkout_session.url},status=status.HTTP_200_OK)

            except Exception as e:
                print(f"Error initiating Stripe payment: {e}")
                return Response({'error': 'Error initiating Stripe payment'}, status=500)

        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        
def process_refund(booking):
    # charge = stripe.Charge.retrieve(booking.stripe_charge_id)
    print('stripe charge id:', booking.stripe_charge_id)
    try:  
        refund = stripe.Refund.create(
            charge=booking.stripe_charge_id
        )
        print(refund)
        print('refund processed')
        # Update booking status and handle any other logic for refund
        update_booking_status(booking, 'cancelled')

    except stripe.error.StripeError as e:
        print(f"Error processing refund: {e}")
        return HttpResponse(status=500)
    

def update_booking_status(booking, new_status):
    booking.status = new_status
    booking.save()


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

        booking_id = session['metadata']['booking_id']
        booking = Booking.objects.get(pk=booking_id)
        # update_booking_status(booking, 'cancelled')
        booking.stripe_charge_id = charge_id
        booking.save()

        if booking.status == 'reserved':
            update_booking_status(booking, 'booked')

        elif booking.status == 'cancelled':
            available_rooms = AvailableRooms.objects.get(room_id=booking.room_id)

            if available_rooms.available_quantity < booking.no_of_rooms:
                available_rooms.available_quantity -= booking.no_of_rooms
                available_rooms.save()

                update_booking_status(booking, 'booked')
            else:
                print('refund processing')
                process_refund(booking)

    return HttpResponse(status=200)


class BookingListView(APIView):
    def get(self, request, tenant_id):
        bookings = Booking.objects.filter(tenant_id=tenant_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
