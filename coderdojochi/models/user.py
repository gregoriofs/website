import os

from django.contrib.auth.models import AbstractUser

# from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

import salesforce
from stdimage.models import StdImageField

from ..notifications import NewMentorBgCheckNotification, NewMentorNotification, NewMentorOrderNotification

# from django.contrib.auth import get_user_model

# User = get_user_model()


def generate_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/<username>
    filename, file_extension = os.path.splitext(filename)
    return f"avatar/{instance.user.username}{file_extension.lower()}"


class CDCUser(salesforce.models.SalesforceModel):

    MENTOR = "mentor"
    GUARDIAN = "guardian"
    STUDENT = "student"

    ROLE_CHOICES = [
        (MENTOR, "mentor"),
        (GUARDIAN, "guardian"),
        (STUDENT, "student"),
    ]

    HISPANIC = "Hispanic"
    NOT_HISPANIC = "Not Hispanic"

    ETHNICITY = [
        (HISPANIC, "Hispanic"),
        (NOT_HISPANIC, "Not Hispanic"),
    ]

    # Common

    role = salesforce.models.CharField(choices=ROLE_CHOICES, max_length=10, db_column="Role__c")

    admin_notes = salesforce.models.TextField(
        blank=True,
        null=True,
        db_column="Admin_Notes__c	",
    )
    first_name = salesforce.models.CharField(max_length=255, db_column="First_Name__c")
    is_active = salesforce.models.BooleanField(
        db_column="Active__c",
        default=True,
    )

    is_public = salesforce.models.BooleanField(
        default=False,
    )

    birthday = salesforce.models.DateField(
        blank=False,
        null=True,
        db_column="Birthdate",
    )

    gender = salesforce.models.CharField(
        max_length=255,
        blank=False,
        null=True,
        db_column="Gender__c",
    )

    ethnicity = salesforce.models.CharField(
        choices=ETHNICITY,
        max_length=255,
        db_column="hed__Ethnicity__c",
        default="",
    )

    race = salesforce.models.CharField(
        max_length=255,
        db_column="hed__Race__c",
        default="",
    )

    phone = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Phone",
    )

    # Mentor-specific

    bio = salesforce.models.TextField(blank=True, null=True, db_column="Description")

    background_check = salesforce.models.BooleanField(
        default=False,
        blank=True,
        null=True,
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

    avatar_approved = salesforce.models.BooleanField(
        blank=True,
        null=True,
        db_column="Avatar_Approved__c",
    )

    work_place = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="GW_Volunteers__Volunteer_Organization__c",
    )

    home_address = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="npe01__Home_Address__c",
    )
    # Guardian

    zip = salesforce.models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    # Student

    parent = salesforce.models.ForeignKey(
        "self",
        limit_choices_to={
            "user__role": GUARDIAN,
        },
        related_name="student_guardian",
        on_delete=salesforce.models.PROTECT,
        blank=True,
        null=True,
        db_column="Parent__c",
    )

    school_name = salesforce.models.CharField(max_length=255, null=True, db_column="School_Name__c")
    school_type = salesforce.models.CharField(max_length=255, null=True, db_column="School_Type__c")
    medical_conditions = salesforce.models.TextField(blank=True, null=True, db_column="Medical__c")
    medications = salesforce.models.TextField(blank=True, null=True, db_column="Medications__c")
    photo_release = salesforce.models.BooleanField(
        "Photo Consent",
        help_text=(
            "I hereby give permission to We All Code to use "
            "the student's image and/or likeness in promotional materials."
        ),
        db_column="Photo_Release__c",
        blank=True,
    )
    consent = salesforce.models.BooleanField(
        "General Consent",
        help_text=("I hereby give consent for the student signed up " "above to participate in We All Code."),
        db_column="Consent__c",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_registered_for_session(self, session):
        from .order import Order

        try:
            Order.objects.get(
                is_active=True,
                student=self,
                session=session,
            )
            is_registered = True
        except Exception:
            is_registered = False

        return is_registered

    def get_age(self, date=timezone.now()):
        return date.year - self.birthday.year - ((date.month, date.day) < (self.birthday.month, self.birthday.day))

    get_age.short_description = "Age"

    def get_clean_gender(self):
        MALE = ["male", "m", "boy", "nino", "masculino"]
        FEMALE = ["female", "f", "girl", "femail", "femal", "femenino"]

        if self.gender.lower() in MALE:
            return "male"
        elif self.gender.lower() in FEMALE:
            return "female"
        else:
            return "other"

    get_clean_gender.short_description = "Clean Gender"

    # returns True if the student age is between minimum_age and maximum_age
    def is_within_age_range(self, minimum_age, maximum_age, date=timezone.now()):
        age = self.get_age(date)

        if age >= minimum_age and age <= maximum_age:
            return True
        else:
            return False

    def is_within_gender_limitation(self, limitation):
        if limitation:
            if self.get_clean_gender() in [limitation.lower(), "other"]:
                return True
            else:
                return False
        else:
            return True

    def get_students(self):

        return CDCUser.objects.filter(
            role=CDCUser.STUDENT,
            guardian=self,
            is_active=True,
        )

    class Meta:
        pass
        # db_table = "Contact"

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("account_home")

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
            orig = CDCUser.objects.get(pk=self.pk, role=CDCUser.MENTOR)
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
