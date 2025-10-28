from booking_service.celery import app
from .models import Booking, AvailableRooms

@app.task
def release_reserved_rooms(booking_id):
    """
    Compensation Flow 2: Timeout - webhook never arrived
    
    This task fires after BOOKING_TIMEOUT_MINUTES if payment
    hasn't completed. Releases the reserved rooms.
    """
    try:
        with transaction.atomic():
            # Use select_for_update to prevent race conditions
            booking = Booking.objects.select_for_update().get(pk=booking_id)
            
            # Idempotency check - only process if still reserved
            if booking.status != 'reserved':
                print(f'Booking {booking_id} already {booking.status}, skipping release')
                return {
                    'status': 'skipped',
                    'reason': f'Booking already {booking.status}'
                }
            
            # Mark as cancelled
            booking.status = 'cancelled'
            booking.save(update_fields=['status', 'updated_at'])
            print(f'Changed booking {booking_id} status to cancelled')
            
            #  ATOMIC INCREMENT - No race condition
            AvailableRooms.objects.filter(room_id=booking.room_id).update(
                available_quantity=F("available_quantity") + booking.no_of_rooms
            )
            print(f'Released {booking.no_of_rooms} rooms back to available pool')
            
            return {
                'status': 'compensated',
                'booking_id': booking_id,
                'rooms_released': booking.no_of_rooms
            }
            
    except Booking.DoesNotExist:
        print(f'Booking {booking_id} not found')
        return {
            'status': 'not_found',
            'booking_id': booking_id
        }
    except Exception as e:
        # ✅ Retry with exponential backoff on failure
        print(f'Error releasing rooms: {e}')
        raise self.retry(exc=e, countdown=2 ** self.request.retries)