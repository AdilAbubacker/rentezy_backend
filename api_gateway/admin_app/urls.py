from django.urls import path
from .views import PropertyRequestsView, ApprovePropertyView, PropertyAdminView, TenantListView, LandlordListView

urlpatterns = [
    path('property-requests/', PropertyRequestsView.as_view()),
    path('approve-property/<str:pk>', ApprovePropertyView.as_view()),
    path('properties/', PropertyAdminView.as_view()),
    path('tenants/', TenantListView.as_view()),
    path('landlords/', LandlordListView.as_view()),
]