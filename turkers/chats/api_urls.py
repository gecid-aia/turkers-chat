from rest_framework_swagger.views import get_swagger_view

from django.urls import path

from chats import api_views as views

schema_view = get_swagger_view(title='Exchange With Turkers API')

app_name = 'chats_api'
urlpatterns = [
    path('', schema_view),
    path('chat/collective/', views.CollectiveChatEndpoint.as_view(), name='collective'),
    path('chat/turker/<int:turker_id>/', views.TurkerChatEndpoint.as_view(), name='turker'),
    path('chat/<int:chat_id>/messages/', views.ListChatMessagesEndpoint.as_view(), name='chat_messages'),
]
