from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from django.http import Http404
from django.shortcuts import get_object_or_404

from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer


class CollectiveChatEndpoint(APIView):

    def get(self, request):
        try:
            chat = Chat.objects.get_collective_chat()
        except Chat.DoesNotExist:
            raise Http404
        serializer = ChatSerializer(instance=chat)
        return Response(serializer.data)


class TurkerChatEndpoint(APIView):

    def get(self, request, turker_id):
        try:
            chat = Chat.objects.get_turker_chat(turker_id)
        except Chat.DoesNotExist:
            raise Http404
        serializer = ChatSerializer(instance=chat)
        return Response(serializer.data)


class ListChatMessagesEndpoint(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'])
        return chat.messages.all()
