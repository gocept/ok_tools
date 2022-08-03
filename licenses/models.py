from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()

MAX_TITLE_LENGTH = 255


class Category(models.Model):
    """
    Model representing a category.

    Each License has a category.
    """

    name = models.CharField(
        _('category'),
        blank=False,
        null=True,
        max_length=255
    )

    def __str__(self) -> str:
        """Represent category by its String."""
        return self.name


def default_category():
    """Provide the default Category."""
    return Category.objects.get_or_create(name=_('Not Selected'))[0]


class LicenseTemplate(models.Model):
    """Fields that are used vor a LicenseRequest and a finished License."""

    title = models.CharField(
        _('title'),
        blank=False,
        null=False,
        max_length=MAX_TITLE_LENGTH,
    )

    subtitle = models.CharField(
        _('subtitle'),
        blank=True,
        null=True,
        max_length=MAX_TITLE_LENGTH,
    )

    description = models.TextField(
        _('description'),
        blank=False,
        null=False,
    )

    duration = models.DurationField(  # timedelta
        _('duration'),
        blank=False,
        null=False,
    )

    suggested_date = models.DateTimeField(  # datetime
        _('suggested broadcast date'),
        blank=True,
        null=True,
    )

    repetitions_allowed = models.BooleanField(
        _('repetitions allowed'),
        blank=False,
        null=False,
    )

    media_authority_exchange_allowed = models.BooleanField(
        _('Media Authority exchange allowed'),
        blank=False,
        null=False,
    )

    youth_protection_necessary = models.BooleanField(
        _('Youth protection necessary'),
        blank=False,
        null=False,
    )

    store_in_ok_media_library = models.BooleanField(
        _('Store in OK media library'),
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        """Licenses are represented by its titles."""
        if self.subtitle:
            return f'{self.title} - {self.subtitle}'
        else:
            return self.title


class LicenseRequest(LicenseTemplate, models.Model):
    """Model representing a license request(Beitragsfreistellung)."""

    okuser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=default_category
    )
