from django.urls import path
from .views import test, RentedPropertiesListView, RentPaymentDeatailsView, RentPaymentView, stripe_webhook

urlpatterns = [
    path('', test),
    path('rented_properties/', RentedPropertiesListView.as_view()),
    path('rented_properties/<str:rent_id>', RentPaymentDeatailsView.as_view()),
    path('webhooks/stripe', stripe_webhook),
    path('pay_monthly_rent', RentPaymentView.as_view()),
]
