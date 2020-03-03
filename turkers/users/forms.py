from django import forms
from django_registration.forms import RegistrationFormTermsOfService

from users.models import User


class UserRegistrationForm(RegistrationFormTermsOfService):
    tos = forms.BooleanField(
        required=True,
        label="You must agree with the ToS (discutir)",  # noqa
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password2")
        self.fields.pop("email")

    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
