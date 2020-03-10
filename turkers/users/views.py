from django.conf import settings
from django.contrib.auth import login
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from django_registration.backends.activation.views import (
    ActivationView as BaseActivationView,
)
from django_registration.backends.one_step.views import RegistrationView

from users.models import User
from users.forms import UserRegistrationForm
from users.recaptcha import validate_captcha


class AboutView(TemplateView):
    template_name = "about.html"


class ToSView(TemplateView):
    template_name = "tos.html"


# Required by activation backend
class ActivationView(BaseActivationView):
    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        login(self.request, user)
        return user


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if not validate_captcha(self.request.POST):
            errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
            errors.append("Invalid Captcha")
            return self.form_invalid(form)

        return super().form_valid(form)

    def register(self, form):
        user = super().register(form)
        login(self.request, user)
        return user


def redirect_turker_to_messages_view(request, turker_uuid):
    if not request.user.is_authenticated:
        user = get_object_or_404(User.objects.turkers(), uuid=turker_uuid)
        login(request, user)
    return redirect(settings.LOGIN_REDIRECT_URL)
