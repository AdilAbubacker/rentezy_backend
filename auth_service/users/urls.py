from django.urls import path
from .views import LoginView, RegisterView, UserView, LogoutView, ValidateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('validate/', ValidateView.as_view()),
    path('logout/', LogoutView.as_view()),
]