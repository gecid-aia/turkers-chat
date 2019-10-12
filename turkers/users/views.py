from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import login

from django_registration.backends.activation.views import ActivationView as BaseActivationView


class AboutView(TemplateView):
    template_name = "about.html"


class ActivationView(BaseActivationView):

    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        login(self.request, user)
        return user
