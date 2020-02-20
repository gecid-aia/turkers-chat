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


class NewChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender', 'content', 'chat', 'reply_to']

    def validate(self, data):
        reply_to = data.get('reply_to')
        chat = data['chat']
        sender = data['sender']

        if reply_to:
            if reply_to.chat_id != chat.id:
               raise serializers.ValidationError("Can't reply to messages from other chats")
            elif not reply_to.user_can_reply(sender):
               raise serializers.ValidationError("User can't reply to this message")

        return data


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['title', 'info', 'is_collective', 'messages_url', 'id']
