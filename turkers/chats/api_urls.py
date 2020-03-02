from rest_framework_swagger.views import get_swagger_view

from django.urls import path

from chats import api_views as views

schema_view = get_swagger_view(title="Exchange With Turkers API")

app_name = "chats_api"
urlpatterns = [
    path("", schema_view),
    path("chats/", views.UserAvailableChatsEndpoint.as_view(), name="chats_index"),
    path("chat/<int:chat_id>/", views.ChatEndpoint.as_view(), name="chat"),
    path(
        "chat/<int:chat_id>/messages/",
        views.ListChatMessagesEndpoint.as_view(),
        name="chat_messages",
    ),
]
