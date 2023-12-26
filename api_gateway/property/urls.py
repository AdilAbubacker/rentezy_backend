from django.urls import path
from .views import PropertyGatewayView, PropertyGatewayPKView

urlpatterns = [
    path('properties/', PropertyGatewayView.as_view()),
    path('properties/<str:pk>', PropertyGatewayPKView.as_view()),
]
