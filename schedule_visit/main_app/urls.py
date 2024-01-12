from django.urls import path
from .views import AvailableTimesAndDatesView, AvailableTimesCreateView, ScheduleVisitView, TenantScheduledVisits

urlpatterns = [
    path('dates_and_times/<int:room_id>', AvailableTimesAndDatesView.as_view()),
    path('available_times/create/', AvailableTimesCreateView.as_view(), name='available-times-create'),
    path('schedule_visit', ScheduleVisitView.as_view()),
    path('scheduled_visits/<int:tenant_id>/', TenantScheduledVisits.as_view(), name='user_scheduled_visits'),
]