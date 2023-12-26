from django.urls import path
from .views import SearchPropertyView, GetPropertyView

urlpatterns = [
    path('search/<str:query>/', SearchPropertyView.as_view()),
    path('properties', GetPropertyView.as_view()),

]