from django.urls import path

from .views import chat

urlpatterns = [
    path('<int:document_id>/', chat, name='chat')
]
