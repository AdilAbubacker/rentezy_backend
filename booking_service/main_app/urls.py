from django.urls import path
from .views import BookingView, StripeCheckoutView

urlpatterns = [
    path('book/', BookingView.as_view()),
    path('stripe/create-checkout-session/', StripeCheckoutView.as_view()),
    # path('', View.as_view()),
    # path('payments/test-payment', test_payment),
]
