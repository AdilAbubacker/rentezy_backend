from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name="test"),
    path('notificationmessages/<int:user_id>/', views.NotificationMessagesView.as_view()),
    path('mark-all-unread-notifications-as-read/<int:user_id>/', views.MarkAllUnreadNotificationsAsRead.as_view()),
]