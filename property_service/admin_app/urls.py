from django.urls import path
from .views import PropertyRequestsView, ApprovePropertyView, PropertyAdminView

urlpatterns = [
    path('property-requests/', PropertyRequestsView.as_view()),
    path('properties/', PropertyAdminView.as_view()),
    path('approve-property/<str:pk>/', ApprovePropertyView.as_view()),
]