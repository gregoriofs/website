import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

from stdimage.models import StdImageField

from ..notifications import NewMentorBgCheckNotification, NewMentorNotification, NewMentorOrderNotification


def generate_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/<username>
    filename, file_extension = os.path.splitext(filename)
    return f"avatar/{instance.user.username}{file_extension.lower()}"


class CDCUser(AbstractUser):

    MENTOR = "mentor"
    GUARDIAN = "guardian"

    ROLE_CHOICES = [
        (MENTOR, "mentor"),
        (GUARDIAN, "guardian"),
    ]

    HISPANIC = "Hispanic"
    NOT_HISPANIC = "Not Hispanic"

    ETHNICITY = [
        (HISPANIC, "Hispanic"),
        (NOT_HISPANIC, "Not Hispanic"),
    ]

    # Common

    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=10,
    
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
        default="",
    )

    race = models.CharField(
        max_length=255,
        # db_column="hed__Race__c",
        default="",
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="Phone",
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

    avatar = StdImageField(
        upload_to=generate_filename,
        blank=True,
        variations={
            "thumbnail": {
                "width": 500,
                "height": 500,
                "crop": True,
            },
        },
        null=True,
    )

    avatar_approved = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )

    work_place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="GW_Volunteers__Volunteer_Organization__c",
    )

    home_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        # db_column="npe01__Home_Address__c",
    )
    # Guardian 
    
    zip = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.full_name

    @property
    def email(self):
        return self.user.email

    def get_students(self):
        from .student import Student

        return Student.objects.filter(
            guardian=self,
            is_active=True,
        )

    class Meta:
        pass
        # db_table = "Contact"

    @cached_property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("account_home")

    # @property
    # def first_name(self):
    #     return self.first_name

    # @property
    # def last_name(self):
    #     return self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def email(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.last_login = timezone.now()

        if self.pk is None and self.role == CDCUser.MENTOR:
            NewMentorNotification(self).send()
        else:
            # FIXME: Update this to match
            orig = CDCUser.objects.get(pk=self.pk, role = CDCUser.MENTOR)
            if orig.avatar != self.avatar:
                self.avatar_approved = False

            if self.background_check is True and orig.background_check != self.background_check:
                NewMentorBgCheckNotification(self).send()

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
