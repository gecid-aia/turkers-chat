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


class TurkerChatEndpointTests(TestCase):

    def setUp(self):
        user = baker.make(User, user_type=User.TK)
        self.client.force_login(user)
        self.chat = baker.make(Chat, turker=user)
        self.url = reverse('chats_api:turker', args=[user.id])

    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_get_chat_data(self):
        response = self.client.get(self.url)
        expected = ChatSerializer(instance=self.chat).data

        assert 200 == response.status_code
        assert expected == response.json()

    def test_404_if_chat_does_not_exist(self):
        self.url = reverse('chats_api:turker', args=[1000])

        response = self.client.get(self.url)

        assert 404 == response.status_code


class ListChatMessagesEndpointTests(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.client.force_login(self.user)
        self.chat = Chat.objects.get_collective_chat()
        self.url = reverse('chats_api:chat_messages', args=[self.chat.id])

    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_404_if_chat_does_not_exist(self):
        self.url = reverse('chats_api:chat_messages', args=[1000])

        response = self.client.get(self.url)

        assert 404 == response.status_code

    def test_get_paginated_messages_data(self):
        messages = baker.make(Message, chat=self.chat, _quantity=42)

        response = self.client.get(self.url)
        data = response.json()

        expected = MessageSerializer(instance=messages[:20], many=True).data
        assert 200 == response.status_code
        assert expected == data['results']
        assert 42 == data['count']
        assert 'next' in data

    def test_add_new_message_on_post(self):
        response = self.client.post(self.url, data={'content': 'new msg'})
        new_msg = Message.objects.first()

        assert 201 == response.status_code
        assert 'new msg' == new_msg.content
        assert MessageSerializer(instance=new_msg).data == response.json()
        assert self.user == new_msg.sender
        assert self.chat == new_msg.chat

    def test_bad_request_if_no_messages(self):
        response = self.client.post(self.url, data={'content': ''})
        assert 400 == response.status_code
        assert 'content' in response.json()

        response = self.client.post(self.url, data={})
        assert 400 == response.status_code
        assert 'content' in response.json()

        assert Message.objects.exists() is False

    def test_404_post_on_unexisting_chat(self):
        self.url = reverse('chats_api:chat_messages', args=[1000])
        response = self.client.post(self.url, data={'content': 'new msg'})
        assert 404 == response.status_code
