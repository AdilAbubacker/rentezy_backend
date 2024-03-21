from django.urls import path
from .views import SearchPropertyView, GetAllPropertiesView, GetPropertyView

urlpatterns = [
    path('<str:query>/', SearchPropertyView.as_view(), name='search-property'),
    path('properties', GetAllPropertiesView.as_view(), name='get-all-properties'),
    path('properties/<int:pk>/', GetPropertyView.as_view(), name='get-property'),
]