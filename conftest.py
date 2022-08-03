from django.core import mail
from django.urls import reverse_lazy
from ok_tools.testing import DOMAIN
from ok_tools.testing import EMAIL
from ok_tools.testing import PWD
from ok_tools.testing import create_user
import ok_tools.wsgi
import pytest
import zope.testbrowser.browser


@pytest.fixture(scope="function")
def browser(db, admin_user):
    """Get a ``zope.testbrowser`` Browser instance.

    Usage:
    >>> browser.open(URL)
    >>> browser.login(USERNAME, PASSWORD)
    """
    return Browser(wsgi_app=ok_tools.wsgi.application)


class Browser(zope.testbrowser.browser.Browser):
    """Browser customized for cookie log-in to admin UI."""

    def login_admin(self):
        """Log-in the admin user."""
        self.open(f'{DOMAIN}{reverse_lazy("admin:login")}')
        self._login('admin@example.com', password='password')

    def login(self, email=EMAIL, password=PWD):
        """Log-in a user."""
        self.open(f'{DOMAIN}{reverse_lazy("login")}')
        self._login(email, password)

    def _login(self, email, password):
        """Log-in a user at the login-page."""
        assert '/login' in self.url, \
            f'Not on login page, URL is {self.url}'
        self.getControl('Email address').value = email
        self.getControl('Password').value = password
        self.getControl('Log in').click()


@pytest.fixture(scope='function')
def mail_outbox():
    """Return the mail outbox."""
    return mail.outbox


@pytest.fixture(scope='function')
def user_dict() -> dict:
    """Return a user as dict."""
    return {
        "email": EMAIL,
        "first_name": "john",
        "last_name": "doe",
        "gender": "m",
        "phone_number": None,
        "mobile_number": None,
        "birthday": "05.09.1989",
        "street": "secondary street",
        "house_number": "1",
        "zipcode": "12345",
        "city": "example-city"
    }


@pytest.fixture(scope='function')
def user(user_dict):
    """Return a registered user with profile and password."""
    return create_user(user_dict)
