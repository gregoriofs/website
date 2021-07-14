import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

import salesforce

from ..notifications import NewMentorBgCheckNotification, NewMentorNotification, NewMentorOrderNotification


def generate_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/<username>
    filename, file_extension = os.path.splitext(filename)
    return f"avatar/{instance.user.username}{file_extension.lower()}"


MENTOR = "mentor"
GUARDIAN = "guardian"

ROLE_CHOICES = [
    (MENTOR, "mentor"),
    (GUARDIAN, "guardian"),
]


HISPANIC = "Hispanic"
NOT_HISPANIC = "Not Hispanic"

ETHNICITY = [
    (HISPANIC,"Hispanic"),
    (NOT_HISPANIC,"Not Hispanic"),
]
    
class CDCUser(AbstractUser):


    # Common

    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=10,
        blank=True,
        null=True,
    )

    admin_notes = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        # db_column="Active__c",
        default=True,
    )

    is_public = models.BooleanField(
        default=False,
    )

    birthday = models.DateField(
        blank=False,
        null=True,
        # db_column="Birthdate",
    )

    gender = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        # db_column="Gender__c",
    )
    
    ethnicity = models.CharField(
        choices=ETHNICITY,
        max_length=255,
        # db_column="hed__Ethnicity__c",
        default=""
    )

    race = models.CharField(
        max_length=255,
        # db_column="hed__Race__c",
        default=""
    )


    # Mentor-specific

    bio = models.TextField(
        blank=True,
        null=True,
        # db_column="Description"
    )

    background_check = models.BooleanField(
        default=False,
        # blank=True,
        # null=True,
    )

    avatar_approved = models.BooleanField(
        default=False,
    ) 

    work_place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="GW_Volunteers__Volunteer_Organization__c",
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="Phone",
    )

    home_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="npe01__Home_Address__c",
    )

    class Meta:
        pass
        # db_table = "Contact"

    @cached_property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    # def get_absolute_url(self):
    #     return reverse("account_home")

    # @property
    # def first_name(self):
    #     return self.user.first_name

    # @property
    # def last_name(self):
    #     return self.user.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # @property
    # def email(self):
    #     return self.email

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.last_login = timezone.now()

        if self.pk is None and self.role == MENTOR:
            NewMentorNotification(self).send()
        else:
            pass
            # FIXME: Update this to match
            # orig = CDCUser.objects.get(pk=self.pk)
            # if orig.avatar != self.avatar:
            #     self.avatar_approved = False

            # if self.background_check is True and orig.background_check != self.background_check:
            #     NewMentorBgCheckNotification(self).send()

        super(CDCUser, self).save(*args, **kwargs)

    def get_approve_avatar_url(self):
        return reverse(
            "mentor-approve-avatar",
            args=[
                str(self.id),
            ],
        )

    def get_reject_avatar_url(self):
        return reverse(
            "mentor-reject-avatar",
            args=[
                str(self.id),
            ],
        )

    def get_avatar(self):
        if (
            self.avatar
            and self.avatar.storage.exists(self.avatar.name)
            and self.avatar.storage.exists(self.avatar.thumbnail.name)
        ):
            return self.avatar

        # Gravatar
        import hashlib
        from urllib.parse import urlencode

        # https://en.gravatar.com/site/implement/images/

        email = self.email.encode("utf-8").lower()
        email_encoded = hashlib.md5(email).hexdigest()

        thumbnail_params = urlencode(
            {
                "d": "mp",
                "r": "g",
                "s": str(320),
            }
        )
        full_params = urlencode(
            {
                "d": "mp",
                "r": "g",
                "s": str(500),
            }
        )
        slug_url = f"https://www.gravatar.com/avatar/{email_encoded}"

        avatar = {
            "url": f"{slug_url}?{full_params}",
            "thumbnail": {
                "url": f"{slug_url}?{thumbnail_params}",
            },
        }

        return avatar
