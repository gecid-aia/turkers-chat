from rest_framework import serializers

from chats.models import Message, Chat


class BaseMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender_username', 'content', 'id']


class MessageSerializer(BaseMessageSerializer):
    reply_to = BaseMessageSerializer()
    accept_reply = serializers.SerializerMethodField()

    class Meta:
        model = BaseMessageSerializer.Meta.model
        fields = BaseMessageSerializer.Meta.fields + ['reply_to', 'accept_reply']

    def get_accept_reply(self, msg):
        user = self.context.get('user', None)
        if not user:
            return False
        return user.is_turker


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['title', 'info', 'is_collective', 'messages_url', 'id']
