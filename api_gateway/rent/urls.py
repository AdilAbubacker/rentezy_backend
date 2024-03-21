from django.urls import path
from .views import RentedPropertiesListView, RentPaymentDeatailsView, RentPaymentView

urlpatterns = [
    path('rented_properties/', RentedPropertiesListView.as_view()),
    path('rented_properties/<str:rent_id>', RentPaymentDeatailsView.as_view()),
    path('pay_monthly_rent', RentPaymentView.as_view()),
]
