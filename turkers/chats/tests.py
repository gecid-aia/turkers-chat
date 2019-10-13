import pytest
from model_bakery import baker
from rest_framework.test import APITestCase as TestCase

from django.urls import reverse

from chats.models import Chat, Message
from chats.serializers import MessageSerializer, ChatSerializer
from users.models import User


class ChatTests(TestCase):

    def setUp(self):
        self.turker = baker.make(User, user_type=User.TK)

    def test_cannot_create_chat_for_regular_user(self):
        assert Chat.objects.get_collective_chat()  # created by initial migration

        chat = Chat(turker=self.turker, info='turker bio')
        chat.save()
        assert chat.id
        assert chat.title == self.turker.username
        assert chat == Chat.objects.get_turker_chat(self.turker.id)

        regular_user = baker.make(User, user_type=User.RG)
        chat = Chat(turker=regular_user)

        with pytest.raises(ValueError):
            chat.save()

        chat = Chat()  # can have only one collective chat
        with pytest.raises(ValueError):
            chat.save()


class MessageSerializerTests(TestCase):

    def setUp(self):
        self.chat = Chat.objects.get_collective_chat()

    def test_serialize_regular_user_message(self):
        user = baker.make(User, user_type=User.RG)
        msg = baker.make(Message, sender=user, content='xpto', chat=self.chat)

        expected = {
            'sender_username': user.username,
            'content': 'xpto',
            'turker_chat_url': '',
        }
        serializer = MessageSerializer(instance=msg)

        assert expected == serializer.data

    def test_serialize_message_for_deleted_user(self):
        user = baker.make(User, user_type=User.RG)
        msg = baker.make(Message, sender=user, content='xpto', chat=self.chat)
        user.delete()
        msg.refresh_from_db()

        expected = {
            'sender_username': 'Anonymous',
            'content': 'xpto',
            'turker_chat_url': '',
        }
        serializer = MessageSerializer(instance=msg)

        assert expected == serializer.data

    def test_serialize_turker_user_message(self):
        user = baker.make(User, user_type=User.TK)
        msg = baker.make(Message, sender=user, content='xpto', chat=self.chat)

        expected = {
            'sender_username': user.username,
            'content': 'xpto',
            'turker_chat_url': reverse('chats_api:turker', args=[user.id]),
        }
        serializer = MessageSerializer(instance=msg)

        assert expected == serializer.data


class ChatSerializerTests(TestCase):

    def test_serialize_chat(self):
        chat = Chat.objects.get_collective_chat()

        expected = {
            'title': 'Collective Chat',
            'info': '',
            'messages_url': reverse('chats_api:chat_messages', args=[chat.id]),
        }
        serializer = ChatSerializer(instance=chat)

        assert expected == serializer.data


class CollectiveChatEndpointTests(TestCase):

    def setUp(self):
        user = baker.make(User)
        self.client.force_login(user)
        self.chat = Chat.objects.get_collective_chat()
        self.url = reverse('chats_api:collective')

    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_get_chat_data(self):
        response = self.client.get(self.url)
        expected = ChatSerializer(instance=self.chat).data

        assert 200 == response.status_code
        assert expected == response.json()

    def test_404_if_chat_is_deleted(self):
        self.chat.delete()

        response = self.client.get(self.url)

        assert 404 == response.status_code
