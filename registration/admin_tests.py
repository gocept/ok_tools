from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from ok_tools.testing import DOMAIN
from ok_tools.testing import create_user
from ok_tools.testing import pdfToText
import pytest
import registration.signals


User = get_user_model()

PWD = 'testpassword'
VERIFIED_PERM = 'registration.verified'


def test__registration__admin__1(browser):
    """It is possible to log in as a valid admin user."""
    browser.login_admin()
    assert 'Site administration' in browser.contents
    assert browser.url == f'{DOMAIN}/admin/'


def test__registration__signals__is_staff__1(db, user_dict):
    """A staff member has the permission 'verified'."""
    testuser = User(email=user_dict['email'], password=PWD, is_staff=True)
    testuser.save()

    assert testuser.has_perm(VERIFIED_PERM)


def test__registration__signals__is_staff__2(db, user, browser):
    """If a user gets staff status he/she has the permission 'verified'."""
    user.profile.verified = True
    user.profile.save()
    browser.login_admin()

    browser.getLink('User').click()
    browser.getLink(user.email).click()
    browser.getControl('Staff status').click()
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert testuser.has_perm(VERIFIED_PERM)


def test__registration__signals__is_staff__3(db, user, browser):
    """If a user is no longer staff, the permission 'verified' gets revoked."""
    user.is_staff = True
    user.save()
    browser.login_admin()

    browser.getLink('User').click()
    browser.getLink(user.email).click()
    browser.getControl('Staff status').click()
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__signals__is_validated__1(db, user, browser):
    """After verification a user has the permission 'verified'."""
    browser.login_admin()
    browser.getLink('Profiles').click()
    browser.getLink(user.email).click()
    browser.getControl('Verified').selected = True
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert testuser.has_perm(VERIFIED_PERM)


def test__registration__signals__is_validated__2(db, user_dict):
    """A User created as verified has the permission 'verified'."""
    user = create_user(user_dict, verified=True)

    testuser = User.objects.get(email=user.email)
    assert testuser.has_perm(VERIFIED_PERM)


def test__registration__signals__is_validated__3(db, user, browser):
    """If a user is no longer verified the permission gets revoked."""
    user.profile.verified = True
    user.profile.save()
    browser.login_admin()

    browser.getLink('Profiles').click()
    browser.getLink(user.email).click()
    browser.getControl('Verified').selected = False
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__signals___get_permission__1(db):
    """
    Helper function '_get_permission'.

    The function raises an error if Permission does not exist.
    """
    with pytest.raises(Permission.DoesNotExist):
        registration.signals._get_permission(Profile, 'testpermission')


def test__registration__admin__UserAdmin__1(db, user, browser):
    """Modify a user without a change."""
    browser.login_admin()

    browser.getLink('User').click()
    browser.getLink(user.email).click()
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__admin__UserAdmin__2(db, user, browser):
    """Modify a user with a change which not changes staff status."""
    browser.login_admin()

    browser.getLink('User').click()
    browser.getLink(user.email).click()
    new_email = 'new_' + user.email
    browser.getControl('Email').value = new_email
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=new_email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__admin__ProfileAdmin__1(db, user, browser):
    """Modify a profile without a change."""
    browser.login_admin()

    browser.getLink('Profile').click()
    browser.getLink(user.email).click()
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__admin__ProfileAdmin__2(db, user, browser):
    """Modify a profile without changing 'verified'."""
    browser.login_admin()

    browser.getLink('Profile').click()
    browser.getLink(user.email).click()

    new_first_name = 'new_' + user.profile.first_name
    browser.getControl('First name').value = new_first_name
    browser.getControl(name='_save').click()

    testuser = User.objects.get(email=user.email)
    assert not testuser.has_perm(VERIFIED_PERM)


def test__registration__admin__verify__1(db, user, user_dict, browser):
    """Verify multiple users."""
    first_email = user.email
    second_email = 'second_' + user_dict['email']
    user_dict['email'] = second_email
    create_user(user_dict)
    browser.login_admin()

    browser.getLink('Profile').click()

    # select both profiles
    browser.getControl(name='_selected_action').controls[0].selected = True
    browser.getControl(name='_selected_action').controls[1].selected = True

    browser.getControl('Action').value = 'verify'
    browser.getControl('Go').click()

    first_user = User.objects.get(email=first_email)
    second_user = User.objects.get(email=second_email)

    assert first_user.profile.verified
    assert second_user.profile.verified
    assert 'successfully verified' in browser.contents


def test__registration__admin__unverify__1(db, user_dict, browser):
    """Unverify multiple users."""
    first_email = user_dict['email']
    create_user(user_dict, verified=True)
    second_email = 'second_' + user_dict['email']
    user_dict['email'] = second_email
    create_user(user_dict, verified=True)
    browser.login_admin()

    browser.getLink('Profile').click()

    # select both profiles
    browser.getControl(name='_selected_action').controls[0].selected = True
    browser.getControl(name='_selected_action').controls[1].selected = True

    browser.getControl('Action').value = 'unverify'
    browser.getControl('Go').click()

    first_user = User.objects.get(email=first_email)
    second_user = User.objects.get(email=second_email)

    assert not first_user.profile.verified
    assert not second_user.profile.verified
    assert 'successfully unverified' in browser.contents


def test__registration__admin__response_change__1(db, user, browser):
    """Print application form."""
    browser.login_admin()

    browser.getLink('Profile').click()
    browser.getLink(user.email).click()
    browser.getControl('Print').click()

    assert browser.headers['Content-Type'] == 'application/pdf'
    assert user.profile.first_name in pdfToText(browser.contents)
    assert user.profile.last_name in pdfToText(browser.contents)
