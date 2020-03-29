import pytest
from model_bakery import baker
from rest_framework.test import APITestCase as TestCase

from django.core.cache import cache
from django.urls import reverse

from chats.models import Chat, Message
from chats.serializers import MessageSerializer, ChatSerializer, NewChatMessageSerializer
from users.models import User, USER_TYPE


class ChatTests(TestCase):
    def setUp(self):
        self.turker = baker.make(User, user_type=USER_TYPE.Turker.value)

    def test_cannot_create_chat_for_regular_user(self):
        assert Chat.objects.get_collective_chat()  # created by initial migration

        chat = self.turker.chat
        assert chat.id
        assert chat.title == self.turker.username

        regular_user = baker.make(User, user_type=USER_TYPE.Regular.value)
        chat = Chat(turker=regular_user)

        with pytest.raises(ValueError):
            chat.save()

        chat = Chat()  # can have only one collective chat
        with pytest.raises(ValueError):
            chat.save()


class MessageSerializerTests(TestCase):
    def setUp(self):
        self.chat = Chat.objects.get_collective_chat()
        self.user = baker.make(User, user_type=USER_TYPE.Regular.value)
        self.ctx = {"user": self.user}

    def test_serialize_regular_user_message(self):
        user = baker.make(User, user_type=USER_TYPE.Regular.value)
        msg = baker.make(Message, sender=user, content="xpto", chat=self.chat)

        expected = {
            "sender_username": user.username,
            "content": "xpto",
            "id": msg.id,
            "reply_to": None,
            "accept_reply": False,
            "sender_is_turker": False,
        }
        serializer = MessageSerializer(instance=msg, context=self.ctx)

        assert expected == serializer.data

    def test_serialize_message_for_deleted_user(self):
        user = baker.make(User, user_type=USER_TYPE.Regular.value)
        msg = baker.make(Message, sender=user, content="xpto", chat=self.chat)
        user.delete()
        msg.refresh_from_db()

        expected = {
            "sender_username": "Anonymous",
            "content": "xpto",
            "id": msg.id,
            "reply_to": None,
            "accept_reply": False,
            "sender_is_turker": False,
        }
        serializer = MessageSerializer(instance=msg, context=self.ctx)

        assert expected == serializer.data

    def test_serialize_turker_user_message(self):
        user = baker.make(User, user_type=USER_TYPE.Turker.value)
        msg = baker.make(Message, sender=user, content="xpto", chat=user.chat)

        expected = {
            "sender_username": user.username,
            "content": "xpto",
            "id": msg.id,
            "reply_to": None,
            "accept_reply": False,
            "sender_is_turker": True,
        }
        serializer = MessageSerializer(instance=msg, context=self.ctx)

        assert expected == serializer.data

    def test_serialize_reply_message(self):
        user = baker.make(User, user_type=USER_TYPE.Turker.value)
        msg = baker.make(
            Message, content="a comment", chat=user.chat, sender__username="foo_user"
        )
        reply = baker.make(
            Message, sender=user, content="xpto", chat=user.chat, reply_to=msg
        )

        expected = {
            "sender_username": user.username,
            "content": "xpto",
            "id": reply.id,
            "accept_reply": False,
            "sender_is_turker": True,
            "reply_to": {
                "sender_username": "foo_user",
                "content": "a comment",
                "id": msg.id,
            },
        }
        serializer = MessageSerializer(instance=reply, context=self.ctx)

        assert expected == serializer.data

    @pytest.mark.skip("Login is no longer required")
    def test_turker_users_can_reply_to_messages(self):
        user = baker.make(User, user_type=USER_TYPE.Regular.value)
        msg = baker.make(Message, sender=user, content="xpto", chat=self.chat)

        self.user.user_type = USER_TYPE.Turker.value
        self.user.save()
        expected = {
            "sender_username": user.username,
            "content": "xpto",
            "id": msg.id,
            "reply_to": None,
            "accept_reply": True,
            "sender_is_turker": False,
        }
        serializer = MessageSerializer(instance=msg, context={"user": self.user})

        assert expected == serializer.data


class ChatSerializerTests(TestCase):
    def setUp(self):
        self.user = baker.make(User, user_type=USER_TYPE.Regular.value)
        self.turker = baker.make(User, user_type=USER_TYPE.Turker.value)

    def test_serialize_collective_chat_for_regular_user(self):
        chat = Chat.objects.get_collective_chat()

        expected = {
            "title": "Only Turkers",
            "info": "",
            "id": chat.id,
            "messages_url": reverse("chats_api:chat_messages", args=[chat.id]),
            "is_collective": True,
            "open_for_messages": False,
        }
        serializer = ChatSerializer(instance=chat, context={"user": self.user})

        assert expected == serializer.data

    def test_serialize_collective_chat_for_turker_user(self):
        chat = Chat.objects.get_collective_chat()

        expected = {
            "title": "Only Turkers",
            "info": "",
            "id": chat.id,
            "messages_url": reverse("chats_api:chat_messages", args=[chat.id]),
            "is_collective": True,
            "open_for_messages": False,
        }
        serializer = ChatSerializer(instance=chat, context={"user": self.turker})

        assert expected == serializer.data

    def test_serialize_turker_chat_for_regular_user(self):
        chat = self.turker.chat

        expected = {
            "title": self.turker.username,
            "info": "",
            "id": chat.id,
            "messages_url": reverse("chats_api:chat_messages", args=[chat.id]),
            "is_collective": False,
            "open_for_messages": False,
        }
        serializer = ChatSerializer(instance=chat, context={"user": self.user})

        assert expected == serializer.data

    def test_serialize_turker_chat_for_turker_user(self):
        chat = self.turker.chat

        expected = {
            "title": self.turker.username,
            "info": "",
            "id": chat.id,
            "messages_url": reverse("chats_api:chat_messages", args=[chat.id]),
            "is_collective": False,
            "open_for_messages": False,
        }
        serializer = ChatSerializer(instance=chat, context={"user": self.turker})

        assert expected == serializer.data


class NewChatMessageSerializerTests(TestCase):
    def setUp(self):
        self.user = baker.make(User, user_type=USER_TYPE.Turker.value)
        self.chat = Chat.objects.get_collective_chat()
        self.data = {
            'sender': self.user.id,
            'content': 'fooooo',
            'chat': self.chat.id,
        }

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_valid_message(self):
        serializer = NewChatMessageSerializer(data=self.data)

        assert serializer.is_valid()

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_clean_message_if_profanity(self):
        self.data['content'] = 'alguma coisa assada'
        serializer = NewChatMessageSerializer(data=self.data)
        assert serializer.is_valid()
        assert serializer.data['content'] == 'alguma coisa assada'

        self.data['content'] = 'your ass'
        serializer = NewChatMessageSerializer(data=self.data)
        assert serializer.is_valid()
        assert serializer.data['content'] == 'your ****'


class ChatEndpointTests(TestCase):
    def setUp(self):
        self.user = baker.make(User, user_type=USER_TYPE.Turker.value)
        self.client.force_login(self.user)
        self.chat = self.user.chat
        self.url = reverse("chats_api:chat", args=[self.chat.id])

    @pytest.mark.skip("Login is no longer required")
    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_get_chat_data(self):
        response = self.client.get(self.url)
        expected = ChatSerializer(instance=self.chat, context={"user": self.user}).data

        assert 200 == response.status_code
        assert expected == response.json()

    def test_404_if_chat_does_not_exist(self):
        self.url = reverse("chats_api:chat", args=[1000])

        response = self.client.get(self.url)

        assert 404 == response.status_code


class ListChatMessagesEndpointTests(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client.force_login(self.user)
        self.turker_user = baker.make(User, user_type=USER_TYPE.Turker.value)
        self.chat = self.turker_user.chat
        self.url = reverse("chats_api:chat_messages", args=[self.chat.id])
        cache.clear()

    @pytest.mark.skip("Login is no longer required")
    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_404_if_chat_does_not_exist(self):
        self.url = reverse("chats_api:chat_messages", args=[1000])

        response = self.client.get(self.url)

        assert 404 == response.status_code

    def test_get_paginated_messages_data(self):
        cache_key = f'chat-{self.chat.id}-messages'
        assert cache.get(cache_key) is None
        messages = baker.make(Message, chat=self.chat, _quantity=42)

        response = self.client.get(self.url)
        data = response.json()

        expected = MessageSerializer(
            instance=messages[::-1][:20], context={"user": self.user}, many=True
        ).data
        assert 200 == response.status_code
        assert expected == data["results"]
        assert 42 == data["count"]
        assert "next" in data
        cached_messages = cache.get(cache_key, default=[])
        for message in messages:
            assert message in cached_messages

    @pytest.mark.skip("Login is no longer required")
    def test_ensure_the_logged_user_is_being_used_in_context(self):
        self.user.user_type = USER_TYPE.Turker.value
        self.user.save()
        baker.make(Message, chat=self.chat, _quantity=42)

        response = self.client.get(self.url)
        data = response.json()

        assert data["results"][0]["accept_reply"] is True

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_add_new_message_on_post(self):
        cache_key = f'chat-{self.chat.id}-messages'
        baker.make(Message, chat=self.chat, _quantity=42)  # add messages to the chat
        self.client.get(self.url)  # populates cache
        assert cache.get(cache_key)  # ensures cache is populated
        self.client.force_login(self.turker_user)

        response = self.client.post(self.url, data={"content": "new msg"})
        new_msg = Message.objects.first()
        expected = MessageSerializer(
            instance=new_msg, context={"user": self.turker_user},
        ).data

        assert 201 == response.status_code
        assert "new msg" == new_msg.content
        assert expected == response.json()
        assert self.turker_user == new_msg.sender
        assert self.chat == new_msg.chat
        assert new_msg.reply_to is None
        assert cache.get(cache_key) is None  # clears cache after new msg

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_reply_to_a_message(self):
        msg = baker.make(Message, chat=self.chat)
        self.user.user_type = USER_TYPE.Turker.value
        self.user.save()

        data = {"content": "new msg", "reply_to": int(msg.id)}
        response = self.client.post(self.url, data=data)
        new_msg = Message.objects.latest("id")
        expected = MessageSerializer(
            instance=new_msg, context={"user": self.user},
        ).data

        assert 201 == response.status_code
        assert "new msg" == new_msg.content
        assert expected == response.json()
        assert self.user == new_msg.sender
        assert self.chat == new_msg.chat
        assert msg == new_msg.reply_to

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_bad_request_if_no_messages(self):
        response = self.client.post(self.url, data={"content": ""})
        assert 400 == response.status_code
        assert "content" in response.json()

        response = self.client.post(self.url, data={"content": "       "})
        assert 400 == response.status_code
        assert "content" in response.json()

        response = self.client.post(self.url, data={})
        assert 400 == response.status_code
        assert "content" in response.json()

        assert Message.objects.exists() is False

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_bad_request_if_reply_to_is_from_another_chat(self):
        other_turker = baker.make(User, user_type=USER_TYPE.Turker.value)
        msg = baker.make(Message, chat=other_turker.chat)
        assert msg.chat != self.chat
        self.user.user_type = USER_TYPE.Turker.value
        self.user.save()

        data = {"content": "new msg", "reply_to": msg.id}
        response = self.client.post(self.url, data=data)

        assert 400 == response.status_code
        assert "non_field_errors" in response.json()

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_bad_request_if_reply_from_regular_user(self):
        msg = baker.make(Message, chat=self.chat)

        data = {"content": "new msg", "reply_to": msg.id}
        response = self.client.post(self.url, data=data)

        assert 400 == response.status_code
        assert "non_field_errors" in response.json()

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_404_post_on_unexisting_chat(self):
        self.url = reverse("chats_api:chat_messages", args=[1000])
        response = self.client.post(self.url, data={"content": "new msg"})
        assert 404 == response.status_code

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_regular_user_can_not_post_on_collective_chat(self):
        chat = Chat.objects.get_collective_chat()
        url = reverse("chats_api:chat_messages", args=[chat.id])

        response = self.client.post(url, data={"content": "hi all turkers!"})

        assert 400 == response.status_code
        assert "non_field_errors" in response.json()

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_turker_user_not_post_on_collective_chat(self):
        chat = Chat.objects.get_collective_chat()
        url = reverse("chats_api:chat_messages", args=[chat.id])
        self.client.force_login(self.turker_user)

        response = self.client.post(url, data={"content": "hi all turkers!"})

        assert 201 == response.status_code

    @pytest.mark.skip("POST operation is no longer allowed.")
    def test_400_if_message_is_to_long(self):
        response = self.client.post(self.url, data={"content": "a" * 1025})

        assert 400 == response.status_code
        assert "content" in response.json()

    def test_405_if_post_request(self):
        response = self.client.post(self.url, data={})
        assert 405 == response.status_code


class ListUserAvailableChatsTests(TestCase):
    def setUp(self):
        self.user = baker.make(User, user_type=USER_TYPE.Regular.value)
        self.client.force_login(self.user)
        self.url = reverse("chats_api:chats_index")

    @pytest.mark.skip("Login is no longer required")
    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        assert 403 == response.status_code

    def test_get_available_chats_for_regular_user(self):
        [
            t.chat
            for t in baker.make(User, user_type=USER_TYPE.Turker.value, _quantity=5)
        ]
        response = self.client.get(self.url)
        expected = ChatSerializer(
            instance=Chat.objects.all(), context={"user": self.user}, many=True
        ).data
        data = response.json()

        assert 200 == response.status_code
        assert len(expected) == len(data['results'])
        for chat in expected:
            assert chat in data['results']

    @pytest.mark.skip("All chats are available")
    def test_get_available_chats_for_turker_user(self):
        self.user.user_type = USER_TYPE.Turker.value
        self.user.save()
        # other turkers
        baker.make(User, user_type=USER_TYPE.Turker.value, _quantity=5)
        turker_chat = baker.make(Chat, turker=self.user)
        collective = Chat.objects.get_collective_chat()

        expected = ChatSerializer(
            instance=[collective, turker_chat], context={"user": self.user}, many=True
        ).data
        response = self.client.get(self.url)
        data = response.json()

        assert 200 == response.status_code
        assert expected == data["results"]
