from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(AbstractUser):
    """
    Model for a Client.

    A Client don't has a username and gets identified by his/her email
    address. Nevertheless the email is optional due to administrative
    reasons of the OKs.
    """

    # If a Client specifiy an email addres it needs to be uniqe
    username = None
    email = models.EmailField(
        _('email address'), blank=True, unique=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
