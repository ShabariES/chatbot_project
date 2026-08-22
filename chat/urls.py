from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('signup/', views.signup_view, name='signup'),
    path('get-response/', views.stream_bot_response, name='get_response'),
    path('clear-history/', views.clear_chat_history, name='clear_chat_history'),
    path('conversations/', views.list_conversations, name='list_conversations'),
    path('conversations/<int:conversation_id>/messages/', views.get_conversation_messages, name='get_conversation_messages'),
    path('conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]