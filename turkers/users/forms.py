from django_registration.forms import RegistrationFormTermsOfService

from users.models import User


class UserRegistrationForm(RegistrationFormTermsOfService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password2')

    class Meta(RegistrationFormTermsOfService.Meta):
        model = User
