from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django_registration.backends.activation.views import RegistrationView

from users.forms import UserRegistrationForm
from users.views import AboutView, ActivationView

urlpatterns = [
    path(r'', include('chats.urls', namespace='chats')),
    path('register/',
        RegistrationView.as_view(form_class=UserRegistrationForm),
        name='django_registration_register',
    ),
    path('activate/complete/',
        TemplateView.as_view(
            template_name='django_registration/activation_complete.html'
        ),
        name='django_registration_activation_complete'),
    path('activate/<activation_key>/',
        ActivationView.as_view(),
        name='django_registration_activate'
    ),
    path(r'', include('django_registration.backends.activation.urls')),
    path(r'', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('sobre/', AboutView.as_view(), name='sobre'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
