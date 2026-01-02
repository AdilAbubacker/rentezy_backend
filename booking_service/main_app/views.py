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
from django.db import transaction, IntegrityError  
from django.db.models import F  
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone 
from celery.result import AsyncResult  
from datetime import datetime, timedelta 

stripe.api_key = settings.STRIPE_SECRET_KEY 

BOOKING_TIMEOUT_MINUTES = 10


# Create your views here.
class BookingView(APIView):
    def post(self, request):
        key = request.headers.get("Idempotency-Key") or request.data.get("idempotency_key")
        if not key:
            return Response({"error": "Idempotency-Key required"}, status=400)

        room_id = request.data.get('room_id')
        tenant_id = request.data.get('tenant_id')
        no_of_rooms = request.data.get('no_of_rooms')
        move_in_date_str = request.data.get('move_in_date')

        if not all([room_id, tenant_id, no_of_rooms]):
            return Response({"error": "Missing required fields"}, status=400)
  
        # parse date
        move_in_date = None
        if move_in_date_str:
            dt = parse_datetime(move_in_date_str)
            if not dt:
                return Response({"error": "Invalid move_in_date format"}, status=400)
            move_in_date = dt.date()

        try:
            no_of_rooms = int(no_of_rooms)
            if no_of_rooms <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "no_of_rooms must be positive integer"}, status=400)

        try:
            available_rooms = AvailableRooms.objects.get(room_id=room_id)
        except AvailableRooms.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)

        if int(available_rooms.available_quantity) < int(no_of_rooms):
            return Response({'error': 'Not enough rooms available'}, status=status.HTTP_400_BAD_REQUEST)
      
        try:
            with transaction.atomic():
                # Create booking in reserved state
                booking, created = Booking.objects.get_or_create(
                    idempotency_key=key,
                    defaults={
                        "room_id": room_id,
                        "tenant_id": tenant_id,
                        "no_of_rooms": no_of_rooms,
                        "move_in_date": move_in_date,
                        "status": "reserved",
                        "expires_at": timezone.now() + timedelta(minutes=BOOKING_TIMEOUT_MINUTES),
                    }
                )

                 # if already existed, try to return existing checkout url (if created). If not, we'll create it safely below.
                if not created:
                    if booking.stripe_session_url:
                        return Response({
                            "booking_id": booking.id,
                            "checkout_url": booking.stripe_session_url,
                            "status": booking.status,
                            "expires_at": booking.expires_at
                        }, status=status.HTTP_200_OK)
                else:
                    # Atomic decrement - prevents race conditions
                    AvailableRooms.objects.filter(room_id=room_id).update(
                        available_quantity=F("available_quantity") - no_of_rooms
                    )

        except IntegrityError as e:
            # Database constraint violated - room quantity went negative
            if "available_quantity_non_negative" in str(e):
                return Response(
                    {'error': 'Not enough rooms available'}, 
                     status=status.HTTP_409_CONFLICT
                )
            return Response(
                {'error': 'Booking failed due to database constraint'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Ensure single release task + single Stripe session creation (serialize using select_for_update)
        try:
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(pk=booking.pk)
                
                # Schedule compensation task and STORE task ID
                if not booking.celery_task_id:
                    task = release_reserved_rooms.apply_async((booking.id,), countdown=BOOKING_TIMEOUT_MINUTES * 60)         
                    booking.celery_task_id = task.id
                    booking.save(update_fields=['celery_task_id'])
                
                # persist Stripe operation-scoped idempotency key
                if not getattr(booking, "stripe_idempotency_key", None):
                    booking.stripe_idempotency_key = f"{booking.idempotency_key}-payment"

                # if another process already created the session while we waited, return it
                if getattr(booking, "stripe_session_url", None):
                    booking.save(update_fields=["celery_task_id", "stripe_idempotency_key"])
                    return Response({
                        "booking_id": booking.id,
                        "checkout_url": booking.stripe_session_url,
                        "status": booking.status,
                        "expires_at": booking.expires_at.isoformat() if booking.expires_at else None
                    }, status=200)

                # Initiate Stripe payment
                unit_amount = int(Decimal(available_rooms.price) * Decimal("100"))
                
                try:
                    checkout_session = stripe.checkout.Session.create(
                        line_items=[
                            {
                                'price_data': {
                                    'currency': 'inr',
                                    'unit_amount':  unit_amount, 
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
                            'amount': unit_amount,
                        },
                        payment_method_types=['card'],
                        mode='payment',
                        success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                        cancel_url=settings.SITE_URL + '/?canceled=true',
                        idempotency_key=booking.stripe_idempotency_key
                    )
                    booking.stripe_session_id = checkout_session.id
                    booking.stripe_session_url = checkout_session.url
                    booking.expires_at = timezone.now() + timedelta(minutes=BOOKING_TIMEOUT_MINUTES)
                    booking.save()
                    return Response({
                        'checkout_url': checkout_session.url,
                        'booking_id': booking.id,
                        'expires_at': booking.expires_at.isoformat(),
                    }, status=status.HTTP_200_OK)

                except Exception as e:
                    # Payment initiation failed - compensate immediately
                    compensate_booking(booking.id)
                    return Response(
                        {'error': 'Error initiating Stripe payment'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )


def compensate_booking(booking_id):
    try:
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(pk=booking_id)
            
            # Idempotency check - only compensate if still reserved
            if booking.status != 'reserved':
                return
            
            # Mark as cancelled
            booking.status = 'cancelled'
            booking.save(update_fields=['status', 'updated_at'])
            
            # ATOMIC INCREMENT - No race condition
            AvailableRooms.objects.filter(room_id=booking.room_id).update(
                available_quantity=F("available_quantity") + booking.no_of_rooms
            )
            
            # Cancel pending Celery task if exists
            if booking.celery_task_id:
                AsyncResult(booking.celery_task_id).revoke()
                
    except Booking.DoesNotExist:
        pass 

        
def process_refund(booking):
    try:  
        refund = stripe.Refund.create(
            charge=booking.stripe_charge_id
        )
        print('refund processed')

        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'updated_at'])
        
        return True

    except stripe.error.StripeError as e:
        print(f"Error processing refund: {e}")
        return False
    

def update_booking_status(booking, new_status):
    booking.status = new_status
    booking.save()


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f'Error parsing payload: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f'Error verifying webhook signature: {e}')
        return HttpResponse(status=400)


    # Change the booking status to reserved on checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        charge_id = session.get('payment_intent')
        booking_id = session['metadata']['booking_id']
        
        try:
            with transaction.atomic():
                booking = Booking.objects.select_for_update().get(pk=booking_id)
                
                # Store charge ID for potential refunds
                booking.stripe_charge_id = charge_id
                booking.save(update_fields=['stripe_charge_id'])
                
                # Idempotency check
                if booking.status == 'booked':
                    return HttpResponse(status=200)  # Already processed
                
                # SUCCESS PATH: Payment succeeded before timeout
                if booking.status == 'reserved':
                    booking.status = 'booked'
                    booking.save(update_fields=['status', 'updated_at'])
                    
                    # Cancel the pending release task
                    if booking.celery_task_id:
                        AsyncResult(booking.celery_task_id).revoke()
                
                # EDGE CASE: Late webhook after timeout cancelled booking
                elif booking.status == 'cancelled':
                    # Try to rebook if rooms available
                    try:
                        with transaction.atomic():
                            updated = AvailableRooms.objects.filter(room_id=booking.room_id).update(
                                available_quantity=F("available_quantity") - booking.no_of_rooms
                            )
                            
                            if updated == 0:
                                raise IntegrityError("Room not found")
                            
                            # Success - rebook
                            booking.status = 'booked'
                            booking.save()
                                
                    except IntegrityError:
                        # Race condition - room taken between check and decrement
                        process_refund(booking)
        
        except Booking.DoesNotExist:
            return HttpResponse(status=404)
    
    # Handle payment failure
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
        booking_id = session['metadata']['booking_id']
        
        # Compensate - release rooms
        compensate_booking(booking_id)
    
    return HttpResponse(status=200)


class BookingListView(APIView):
    def get(self, request, tenant_id):
        bookings = Booking.objects.filter(tenant_id=tenant_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
