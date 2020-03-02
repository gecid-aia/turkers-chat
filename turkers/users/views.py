from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings

from django_registration.backends.activation.views import (
    ActivationView as BaseActivationView,
)
from django_registration.backends.one_step.views import RegistrationView
from django_registration.forms import RegistrationForm

from users.models import User


class AboutView(TemplateView):
    template_name = "about.html"


# Required by activation backend
class ActivationView(BaseActivationView):
    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        login(self.request, user)
        return user


class UserRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
        ]


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm

    def register(self, form):
        user = super().register(form)
        login(self.request, user)
        return user


def redirect_turker_to_messages_view(request, turker_uuid):
    if not request.user.is_authenticated:
        user = get_object_or_404(User.objects.turkers(), uuid=turker_uuid)
        login(request, user)
    return redirect(settings.LOGIN_REDIRECT_URL)
