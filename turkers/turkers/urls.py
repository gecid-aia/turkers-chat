from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect

from django_registration.backends.activation.views import RegistrationView

from users.forms import UserRegistrationForm
from users.views import (
    AboutView,
	SobreView,
    ToSView,
    UserRegistrationView,
    redirect_turker_to_messages_view,
)


def custom_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
    else:
        return LoginView.as_view()(request)


urlpatterns = [
    path(r"", include("chats.urls", namespace="chats")),
    path(r"api/", include("chats.api_urls", namespace="chats_api")),
    #   LEAVE THIS TO EASILY RESTORE ACTIVATION IF NEEDED
    #    path('register/',
    #        RegistrationView.as_view(form_class=UserRegistrationForm),
    #        name='django_registration_register',
    #    ),
    #    path('activate/complete/',
    #        TemplateView.as_view(
    #            template_name='django_registration/activation_complete.html'
    #        ),
    #        name='django_registration_activation_complete'),
    #    path('activate/<activation_key>/',
    #        ActivationView.as_view(),
    #        name='django_registration_activate'
    #    ),
    path(
        r"register/",
        UserRegistrationView.as_view(success_url="/"),
        name="django_registration_register",
    ),
    path(r"", include("django_registration.backends.one_step.urls")),
    path(r"login/", custom_login, name="login"),
    path(r"", include("django.contrib.auth.urls")),
    path(
        "access/<uuid:turker_uuid>/",
        redirect_turker_to_messages_view,
        name="redirect_turker",
    ),
    path("admin/", admin.site.urls),
    path("about/", AboutView.as_view(), name="about"),
	path("sobre/", SobreView.as_view(), name="sobre"),
    path("tos/", ToSView.as_view(), name="tos"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
