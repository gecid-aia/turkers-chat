from django.test import TestCase

from users.forms import UserRegistrationForm


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
