from django.urls import path
from .views import PromoteToLandlordView, TenantListView, LandlordListView

urlpatterns = [
    path('promote_to_landlord/<str:pk>/', PromoteToLandlordView.as_view()),
    path('tenants/', TenantListView.as_view()),
    path('landlords/', LandlordListView.as_view()),
]
