from django.urls import path

from chats import views


app_name = "chats"
urlpatterns = [
    path("", views.chats_index, name="index"),
]
