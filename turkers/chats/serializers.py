from rest_framework import serializers

from chats.models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender_username', 'content', 'turker_chat_url']


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['title', 'info', 'messages_url', 'is_collective']
