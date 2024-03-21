from django.urls import include, path
from .views import RegisterUserView, LoginView, LogoutView, UserView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]