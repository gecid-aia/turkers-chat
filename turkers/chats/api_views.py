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

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'])

        content = str(request.data.get('content', ''))
        if not content:
            return Response({'content': 'A new message must have content.'}, status=400)

        new_msg = chat.messages.create(
            sender=request.user,
            content=content
        )
        return Response(self.serializer_class(instance=new_msg).data, status=201)
