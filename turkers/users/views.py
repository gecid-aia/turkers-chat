from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings

from django_registration.backends.activation.views import (
    ActivationView as BaseActivationView,
)
from django_registration.backends.one_step.views import RegistrationView

from users.models import User
from users.forms import UserRegistrationForm


class AboutView(TemplateView):
    template_name = "about.html"


# Required by activation backend
class ActivationView(BaseActivationView):
    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        login(self.request, user)
        return user


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
