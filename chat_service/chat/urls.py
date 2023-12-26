from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index),
    # path("<str:room_name>/", views.room, name="room"),
    path('create/',views.MessageCreateView.as_view(),name='message-create'),
    path('chatmessages/<int:tenant_id>/<int:landlord_id>/', views.ChatMessagesView.as_view()),
]
