from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AvailableTimes, TimeSlot
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from .models import AvailableTimes, TimeSlot, ScheduledVisit
import json
from django.utils import timezone
from calendar import month_abbr

MONTH_ABBR_TO_NUM = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}


class AvailableTimesAndDatesView(APIView):
    def get(self, request, room_id):

        # Get available times for each room
        room = AvailableTimes.objects.get(room_id=room_id)
        times = room.times.values_list('time', flat=True)

        # Get dates of next seven days
        today = datetime.now()
        next_seven_days = [today + timedelta(days=i) for i in range(1, 8)]

        formatted_dates = [
                {
                    'month': date.strftime('%b'),
                    'day': date.strftime('%d'),
                    'weekday': date.strftime('%a')
                }
                for date in next_seven_days
            ]
        
        data = {
            'times':list(times),
            'dates':formatted_dates
        }
        return Response(data, status=status.HTTP_200_OK)



class AvailableTimesCreateView(APIView):
    def post(self, request, *args, **kwargs):
        room_id = request.data.get('room_id')
        times  = request.data.get('times')

        if room_id is None or times is None:
            return JsonResponse({'error': 'Invalid data format'}, status=400)

        # Get or create AvailableTimes instance for the room
        room, created = AvailableTimes.objects.get_or_create(room_id=room_id)
        time_slots = []

        for time_str in times:
            time_slot, created = TimeSlot.objects.get_or_create(time=time_str)
            room.times.add(time_slot)
            time_slots.append(time_str)

        return JsonResponse({'room_id': room.room_id, 'times': time_slots}, status=status.HTTP_201_CREATED)
    

class ScheduleVisitView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            selected_time = data.get('selected_time')
            visitor_id = data.get('tenant_id')
            visit_date = data.get('selected_date')

            if room_id is None or selected_time is None or visitor_id is None or visit_date is None:
                return JsonResponse({'error': 'Invalid data format'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                room = AvailableTimes.objects.get(room_id=room_id)
                time_slot = TimeSlot.objects.get(time=selected_time)

                # Extract day, month, and year from the selected_date
                day = int(visit_date['day'])
                month = MONTH_ABBR_TO_NUM.get(visit_date['month'])
                year = datetime.now().year  # Assuming the current year

                # Combine day, month, and year into a valid date format
                date_str = f"{year}-{month:02d}-{day:02d}"
                visit_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                # Check if the selected time is available
                if time_slot in room.times.all():
                    # Schedule the visit by creating a ScheduledVisit instance or retrieving an existing one
                    scheduled_visit, created = ScheduledVisit.objects.get_or_create(
                        room=room,
                        visitor_id=visitor_id,
                        defaults={
                            'time_slot': time_slot,
                            'visit_date': visit_date
                        }
                    )

                    # If the visit already existed, update the time_slot and visit_date
                    if not created:
                        scheduled_visit.time_slot = time_slot
                        scheduled_visit.visit_date = visit_date
                        scheduled_visit.save()

                        return JsonResponse({'success': 'Visit updated successfully'}, status=status.HTTP_205_RESET_CONTENT)

                    return JsonResponse({'success': 'Visit created successfully'}, status=status.HTTP_201_CREATED)

                return JsonResponse({'error': 'Selected time is not available'}, status=400)

            except AvailableTimes.DoesNotExist:
                return JsonResponse({'error': 'Room not found'}, status=404)
            except TimeSlot.DoesNotExist:
                return JsonResponse({'error': 'Invalid time slot'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        

class TenantScheduledVisits(APIView):
    def get(self, request, tenant_id):
        try:
            # Get current date and time
            current_datetime = timezone.now()

            # Get scheduled visits for a user
            user_scheduled_visits = ScheduledVisit.objects.filter(visitor_id=tenant_id)

            # Categorize visits into previous and upcoming
            previous_visits = []
            upcoming_visits = []

            for visit in user_scheduled_visits:
                if visit.visit_date < current_datetime.date():
                    previous_visits.append({
                        'visitor_id': visit.visitor_id,
                        'room_id': visit.room.room_id,
                        'time': visit.time_slot.time,
                        'visit_date': visit.visit_date,
                        'title': visit.title
                    })
                else:
                    upcoming_visits.append({
                        'visitor_id': visit.visitor_id,
                        'room_id': visit.room.room_id,
                        'time': visit.time_slot.time,
                        'visit_date': visit.visit_date,
                        'title': visit.title
                    })

            data = {
                'previous_visits': previous_visits,
                'upcoming_visits': upcoming_visits,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)