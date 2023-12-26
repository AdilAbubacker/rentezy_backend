from django.urls import path
from .views import PropertyViewSet

urlpatterns = [
    path('properties/', PropertyViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path('properties/<str:pk>', PropertyViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
]