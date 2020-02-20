from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.http import Http404
from django.shortcuts import get_object_or_404

from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer


class ChatEndpoint(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_url_kwarg = 'chat_id'


class ListChatMessagesEndpoint(ListAPIView):
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

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


class UserAvailableChatsEndpoint(ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_regular:
            return Chat.objects.all()
        elif user.is_turker:
            return [
                Chat.objects.get_collective_chat(),
                Chat.objects.get_turker_chat(user.id)
            ]
