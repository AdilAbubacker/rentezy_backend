from django.urls import path
from .views import SearchPropertyView, GetAllPropertiesView, GetPropertyView

urlpatterns = [
    path('search/<str:query>/', SearchPropertyView.as_view()),
    path('properties', GetAllPropertiesView.as_view()),
    path('properties/<int:pk>/', GetPropertyView.as_view()),
]