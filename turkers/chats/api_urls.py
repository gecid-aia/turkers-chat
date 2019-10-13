from rest_framework_swagger.views import get_swagger_view

from django.urls import path

from chats import api_views as views

schema_view = get_swagger_view(title='Exchange With Turkers API')

app_name = 'chats_api'
urlpatterns = [
    path('', schema_view),
    path('chat/colective/', views.ColectiveChatEndpoint.as_view(), name='colective'),
    path('chat/turker/<int:turker_id>/', views.ColectiveChatEndpoint.as_view(), name='turker'),
]
