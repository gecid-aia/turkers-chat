from rest_framework import serializers

from chats.models import Message, Chat


class BaseMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender_username", "content", "id"]


class MessageSerializer(BaseMessageSerializer):
    reply_to = BaseMessageSerializer()
    accept_reply = serializers.SerializerMethodField()

    class Meta:
        model = BaseMessageSerializer.Meta.model
        fields = BaseMessageSerializer.Meta.fields + [
            "reply_to",
            "accept_reply",
            "sender_is_turker",
        ]

    def get_accept_reply(self, msg):
        user = self.context.get("user", None)
        return msg.user_can_reply(user)


class NewChatMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True, max_length=1024)

    class Meta:
        model = Message
        fields = ["sender", "content", "chat", "reply_to"]

    def validate(self, data):
        reply_to = data.get("reply_to")
        chat = data["chat"]
        sender = data["sender"]

        if not chat.user_can_post(sender):
            raise serializers.ValidationError(
                "User is not allowed to post new messages in this chat"
            )
        if reply_to:
            if reply_to.chat_id != chat.id:
                raise serializers.ValidationError(
                    "Can't reply to messages from other chats"
                )
            elif not reply_to.user_can_reply(sender):
                raise serializers.ValidationError("User can't reply to this message")

        return data


class ChatSerializer(serializers.ModelSerializer):
    open_for_messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "title",
            "info",
            "is_collective",
            "messages_url",
            "id",
            "open_for_messages",
        ]

    def get_open_for_messages(self, chat):
        user = self.context.get("user", None)
        return chat.user_can_post(user)
