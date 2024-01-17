from django.urls import path
from .views import BookingView, stripe_webhook, BookingListView

urlpatterns = [
    path('book/', BookingView.as_view()),
    path('webhooks/stripe/', stripe_webhook),
    path('booking_listings/', BookingListView.as_view()),

]
