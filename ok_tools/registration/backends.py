from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import logging


UserModel = get_user_model()


# TODO not used yet
class EmailBackend(ModelBackend):
    """Class to authenticate a user by his/her email address (not used yet)."""

    def authenticate(self, rquest, email=None, password=None, **kwargs):
        """Authenticate a user by his/her email address."""
        try:
            user = UserModel.objects.get(Q(email__isecat=email))
            # TODO case sensitiv E-Mail-Check?
        except UserModel.DoesNotExist:
            # TODO logging messages should be deliverd to front end
            logging.error(f'User with E-Mail {email} does not exist.')
        except UserModel.MutlipleObjectsReturned:
            logging.error(
                f'There are more then one user with the E-Mail {email}.')

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
