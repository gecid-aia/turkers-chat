import pytest
from model_bakery import baker

from django.test import TestCase

from chats.models import Chat
from users.models import User


class ChatTests(TestCase):

    def setUp(self):
        self.turker = baker.make(User, user_type=User.TK)

    def test_cannot_create_chat_for_regular_user(self):
        chat = Chat()  # without turker == colective chat
        chat.save()
        assert chat.id
        assert chat.title == 'Colective Chat'
        assert chat == Chat.objects.get_colective_chat()

        chat = Chat(turker=self.turker, info='turker bio')
        chat.save()
        assert chat.id
        assert chat.title == self.turker.username
        assert chat == Chat.objects.get_turker_chat(self.turker.id)

        regular_user = baker.make(User, user_type=User.RG)
        chat = Chat(turker=regular_user)

        with pytest.raises(ValueError):
            chat.save()

        chat = Chat()  # can have only one colective chat
        with pytest.raises(ValueError):
            chat.save()
