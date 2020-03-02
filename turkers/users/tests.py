from model_bakery import baker

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegistrationForm
from users.models import User, USER_TYPE


class UserRegistrationFormTests(TestCase):
    def setUp(self):
        self.data = {
            "username": "foo",
            "email": "foo@foo.com",
            "password1": "myverysecurepassword",
            "tos": True,
        }

    def test_registration_form_create_regular_user(self):
        form = UserRegistrationForm(self.data)
        assert form.is_valid(), form.errors
        user = form.save()
        assert user.is_regular
        assert user.check_password("myverysecurepassword")

    def test_tos_is_required(self):
        self.data["tos"] = False
        form = UserRegistrationForm(self.data)
        assert form.is_valid() is False
        assert "tos" in form.errors


class RedirectTurkerUserToMessagesTests(TestCase):
    def setUp(self):
        self.turker_user = baker.make(User, user_type=USER_TYPE.Turker.value)
        self.url = reverse("redirect_turker", args=[self.turker_user.uuid])

    def test_redirect_turker_to_index(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        assert '_auth_user_id' in self.client.session
        assert int(self.client.session['_auth_user_id']) == self.turker_user.pk

    def test_404_if_user_does_not_exist(self):
        self.turker_user.delete()

        response = self.client.get(self.url)

        assert 404 == response.status_code

    def test_404_if_user_is_not_turker(self):
        self.turker_user.user_type = USER_TYPE.Regular.value
        self.turker_user.save()

        response = self.client.get(self.url)

        assert 404 == response.status_code

    def test_redirect_user_if_logged(self):
        user = baker.make(User, user_type=USER_TYPE.Regular.value)
        self.client.force_login(user)

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        assert '_auth_user_id' in self.client.session
        assert int(self.client.session['_auth_user_id']) == user.pk
