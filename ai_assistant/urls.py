from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_dashboard, name='ai_dashboard'),
    path("chat/", views.ai_chat, name="ai_chat_new"),
    path('new/', views.ai_new_chat, name='ai_new_chat'),

    path('chat/<int:pk>/', views.ai_chat, name='ai_chat'),
    path('delete-all/', views.ai_delete_all_conversations, name='ai_delete_all_conversations'),

    path('delete/<int:pk>/', views.ai_delete_conversation, name='ai_delete_conversation'),
    path('api/chat/', views.ai_chat_api, name='ai_chat_api'),
]