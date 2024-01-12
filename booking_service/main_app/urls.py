from django.urls import path
from .views import BookingView, stripe_webhook

urlpatterns = [
    path('book/', BookingView.as_view()),
    path('webhooks/stripe/', stripe_webhook),
]
