from django.urls import path
from .views import LoginView, RegisterView, UserView, LogoutView, ValidateView, GetUsernamesAPIView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('validate/', ValidateView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('get_usernames/', GetUsernamesAPIView.as_view(), name='get_usernames')
]