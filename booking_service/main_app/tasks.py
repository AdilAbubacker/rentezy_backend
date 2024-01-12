from booking_service.celery import app
from .models import Booking, AvailableRooms

@app.task
def release_reserved_rooms(booking_id):
    # Release the reserved rooms after 10 minutes if payment hasn't taken place
    print('__________1______')
    booking = Booking.objects.get(pk=booking_id)
    if booking.status == 'Reserved':
        booking.status = 'Cancelled'
        booking.save()
        print('changed booking status to cancelled')
        
        # Release the reserved rooms in AvailableRooms model
        available_rooms = AvailableRooms.objects.get(room_id=booking.room_id)
        available_rooms.available_quantity += booking.no_of_rooms
        print('released rooms to other users')
        available_rooms.save()