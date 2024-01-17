from django.urls import path
from .views import test, RentedPropertiesListView, RentPaymentDeatailsView

urlpatterns = [
    path('', test),
    path('rented_properties/', RentedPropertiesListView.as_view()),
    path('rented_properties/<str:rent_id>', RentPaymentDeatailsView.as_view()),
]
