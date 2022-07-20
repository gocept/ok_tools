"""ok_tools URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView
from registration.views import PasswordResetConfirmView
from registration.views import PasswordResetView
from registration.views import RegisterView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path(
        "profile/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path('profile/password_reset/',
         PasswordResetView.as_view(),
         name='password_reset'
         ),
    path('profile/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'profile/created',
        TemplateView.as_view(template_name='registration/user_created.html'),
        name='user_created'),
    path(
        'terms_of_condition/',
        TemplateView.as_view(template_name='toc.html'),
        name='toc'
    ),
]
