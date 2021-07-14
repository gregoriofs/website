# import os

# #from django.db import models
# from django.urls import reverse

# from stdimage.models import StdImageField

# from ..notifications import NewMentorBgCheckNotification, NewMentorNotification, NewMentorOrderNotification
# from .common import CommonInfo
# from .race_ethnicity import RaceEthnicity
# from .user import CDCUser

# import salesforce

# # def generate_filename(instance, filename):
# #     # file will be uploaded to MEDIA_ROOT/avatar/<username>
# #     filename, file_extension = os.path.splitext(filename)
# #     return f"avatar/{instance.user.username}{file_extension.lower()}"


# # TODO: Add MentorManager
# # class Mentor(salesforce.models.SalesforceModel):
# #     # Mentor(CommonInfo)
    
# #     HISPANIC = "Hispanic"
# #     NOT_HISPANIC = "Not Hispanic"

# #     ETHNICITY = [
# #         (HISPANIC,"Hispanic"),
# #         (NOT_HISPANIC,"Not Hispanic"),
# #     ]

# #     user = salesforce.models.ForeignKey(
# #         CDCUser,
# #         on_delete=salesforce.models.PROTECT,
# #     )
# #     bio = salesforce.models.TextField(
# #         blank=True,
# #         null=True,
# #         db_column="Description"
# #     )
    
# #     is_active = salesforce.models.BooleanField(
# #         db_column="Active__c",
# #         default=True,
# #     )
# #     background_check = salesforce.models.BooleanField(
# #         default=False,
# #     )
# #     is_public = salesforce.models.BooleanField(
# #         default=False,
# #     )
# #     # avatar = StdImageField(
# #     #     upload_to=generate_filename,
# #     #     blank=True,
# #     #     variations={
# #     #         "thumbnail": {
# #     #             "width": 500,
# #     #             "height": 500,
# #     #             "crop": True,
# #     #         },
# #     #     },
# #     # )
# #     avatar_approved = salesforce.models.BooleanField(
# #         default=False,
# #     )
# #     birthday = salesforce.models.DateField(
# #         blank=False,
# #         null=True,
# #         db_column="Birthdate",
# #     )
# #     gender = salesforce.models.CharField(
# #         max_length=255,
# #         blank=False,
# #         null=True,
# #         db_column="Gender__c",
# #     )
# #     #Many to Many field in salesforce?
# #     # race_ethnicity = models.ManyToManyField(
# #     #     RaceEthnicity,
# #     #     blank=False,
# #     # )
# #     ethnicity = salesforce.models.CharField(
# #         choices=ETHNICITY,
# #         max_length=255,
# #         db_column="hed__Ethnicity__c",
# #         default=""
# #     )
# #     race = salesforce.models.CharField(
# #         max_length=255,
# #         db_column="hed__Race__c",
# #         default=""
# #     )

# #     work_place = salesforce.models.CharField(
# #         max_length=255,
# #         blank=True,
# #         null=True,
# #         db_column="GW_Volunteers__Volunteer_Organization__c",
# #     )
# #     phone = salesforce.models.CharField(
# #         max_length=255,
# #         blank=True,
# #         null=True,
# #         db_column="Phone",
# #     )
# #     home_address = salesforce.models.CharField(
# #         max_length=255,
# #         blank=True,
# #         null=True,
# #         db_column="npe01__Home_Address__c",
# #     )

# #     def __str__(self):
# #         return self.full_name

# #     class Meta:
# #         db_table = "Contact"

# #     @property
# #     def first_name(self):
# #         return self.user.first_name

# #     @property
# #     def last_name(self):
# #         return self.user.last_name

# #     @property
# #     def full_name(self):
# #         return f"{self.user.first_name} {self.user.last_name}"

# #     @property
# #     def email(self):
# #         return self.user.email

# #     def save(self, *args, **kwargs):
# #         if self.pk is None:
# #             NewMentorNotification(self).send()
# #         else:
# #             orig = Mentor.objects.get(pk=self.pk)
# #             if orig.avatar != self.avatar:
# #                 self.avatar_approved = False

# #             if self.background_check is True and orig.background_check != self.background_check:
# #                 NewMentorBgCheckNotification(self).send()

# #         super(Mentor, self).save(*args, **kwargs)

# #     def get_approve_avatar_url(self):
# #         return reverse(
# #             "mentor-approve-avatar",
# #             args=[
# #                 str(self.id),
# #             ],
# #         )

# #     def get_reject_avatar_url(self):
# #         return reverse(
# #             "mentor-reject-avatar",
# #             args=[
# #                 str(self.id),
# #             ],
# #         )

# #     def get_absolute_url(self):
# #         return reverse(
# #             "mentor-detail",
# #             args=[
# #                 str(self.id),
# #             ],
# #         )

# #     def get_avatar(self):
# #         if (
# #             self.avatar
# #             and self.avatar.storage.exists(self.avatar.name)
# #             and self.avatar.storage.exists(self.avatar.thumbnail.name)
# #         ):
# #             return self.avatar

# #         # Gravatar
# #         import hashlib
# #         from urllib.parse import urlencode

# #         # https://en.gravatar.com/site/implement/images/

# #         email = self.email.encode("utf-8").lower()
# #         email_encoded = hashlib.md5(email).hexdigest()

# #         thumbnail_params = urlencode(
# #             {
# #                 "d": "mp",
# #                 "r": "g",
# #                 "s": str(320),
# #             }
# #         )
# #         full_params = urlencode(
# #             {
# #                 "d": "mp",
# #                 "r": "g",
# #                 "s": str(500),
# #             }
# #         )
# #         slug_url = f"https://www.gravatar.com/avatar/{email_encoded}"

# #         avatar = {
# #             "url": f"{slug_url}?{full_params}",
# #             "thumbnail": {
# #                 "url": f"{slug_url}?{thumbnail_params}",
# #             },
# #         }

# #         return avatar
