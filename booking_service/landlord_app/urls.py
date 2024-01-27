from django.urls import path
from .views import BookingListView

urlpatterns = [
    path('booking_listings/', BookingListView.as_view()),
]
