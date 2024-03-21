from . import views
from django.urls import path

urlpatterns = [
    path('create/',views.MessageCreateView.as_view(),name='message-create'),
    path('chatmessages/<int:tenant_id>/<int:landlord_id>/', views.ChatMessagesView.as_view()),
    path('users_chatted_with/<int:user_id>/', views.UsersChattedWithView.as_view(), name='users-chatted-with'),
]
