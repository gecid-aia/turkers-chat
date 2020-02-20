from rest_framework import serializers

from chats.models import Message, Chat


class BaseMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender_username', 'content', 'id']


class MessageSerializer(BaseMessageSerializer):
    reply_to = BaseMessageSerializer()

    class Meta:
        model = BaseMessageSerializer.Meta.model
        fields = BaseMessageSerializer.Meta.fields + ['reply_to']


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['title', 'info', 'is_collective', 'messages_url', 'id']
