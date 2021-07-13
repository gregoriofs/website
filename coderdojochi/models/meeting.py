# from django.db import models
from django.urls import reverse
from django.utils import formats
import salesforce
# from django.db import models

from .common import CommonInfo
from .location import Location
from .mentor import Mentor


class MeetingType(salesforce.models.SalesforceModel):
    # class MeetingType(CommonInfo):
    code = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Code__c"
    )
    title = salesforce.models.CharField(
        max_length=255,
        db_column="Title__c"
    )
    # slug = models.SlugField(
    #     max_length=40,
    #     blank=True,
    #     null=True,
    # )
    description = salesforce.models.TextField(
        blank=True,
        null=True,
        help_text="Basic HTML allowed",
        db_column="Description__c"
    )

    class Meta:
        db_table="Meeting_Type__c"
        managed=True

    def __str__(self):
        if self.code:
            return f"{self.code} | {self.title}"

        return f"{self.title}"

class Meeting(salesforce.models.SalesforceModel):
# class Meeting(CommonInfo):

    meeting_type = salesforce.models.ForeignKey(
        MeetingType,
        on_delete=salesforce.models.PROTECT,
        db_column="Meeting_Type__c"
    )
    additional_info = salesforce.models.TextField(
        blank=True,
        null=True,
        help_text="Basic HTML allowed",
        db_column="Additional_Information__c"
    )
    start_date = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        db_column="Start_Date__c"
    )
    end_date = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        db_column="End_Date__c"
    )
    location = salesforce.models.ForeignKey(
        Location,
        on_delete=salesforce.models.PROTECT,
        db_column="Address__c",
        default=""
    )
    external_enrollment_url = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="When provided, local enrollment is disabled.",
        db_column="External_Enrollment_URL__c"
    )
    is_public = salesforce.models.BooleanField(
        db_column="Is_Public__c"
    )
    is_active = salesforce.models.BooleanField(
        db_column="Is_Active__c",
    )
    image_url = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Image_URL__c"
    )
    # bg_image = models.ImageField(
    #     blank=True,
    #     null=True,
    # )
    announced_date = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        db_column="Announced_Date__c"
    )

    class Meta:
        db_table="Meeting__c"
        managed=True

    def __str__(self):
        date = formats.date_format(self.start_date, "SHORT_DATETIME_FORMAT")
        return f"{self.meeting_type.title} | {date}"

    def get_absolute_url(self):
        return reverse("meeting-detail", args=[str(self.id)])

    def get_sign_up_url(self):
        return reverse("meeting-register", args=[str(self.id)])

    def get_calendar_url(self):
        return reverse("meeting-calendar", args=[str(self.id)])

    def get_current_orders(self, checked_in=None):
        if checked_in is not None:
            if checked_in:
                orders = (
                    MeetingOrder.objects.filter(
                        is_active=True,
                        meeting=self,
                    )
                    .exclude(
                        check_in=None,
                    )
                    .order_by("mentor__user__last_name")
                )
            else:
                orders = MeetingOrder.objects.filter(
                    is_active=True,
                    meeting=self,
                    check_in=None,
                ).order_by("mentor__user__last_name")

        else:
            orders = MeetingOrder.objects.filter(is_active=True, meeting=self,).order_by(
                "check_in",
                "mentor__user__last_name",
            )

        return orders

    def get_current_mentors(self):
        return Mentor.objects.filter(
            id__in=MeetingOrder.objects.filter(is_active=True, meeting=self,).values(
                "mentor__id",
            )
        )

    def get_mentor_count(self):
        return MeetingOrder.objects.filter(meeting__id=self.id).count()

    get_mentor_count.short_description = "Mentors"


class MeetingOrder(salesforce.models.SalesforceModel):
#class MeetingOrder(CommonInfo):

    mentor = salesforce.models.ForeignKey(
        Mentor,
        on_delete=salesforce.models.PROTECT,
        db_column="Mentor__c"
    )
    meeting = salesforce.models.ForeignKey(
        Meeting,
        on_delete=salesforce.models.PROTECT,
        db_column="Meeting__c"
    )

    is_active = salesforce.models.BooleanField(
        db_column="Is_Active__c",
    )

    ip = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="IP__c"
    )

    check_in = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        db_column="Check_In__c"
    )

    affiliate = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Affiliate__c"
    )

    order_number = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Order_Number__c"
    )

    week_reminder_sent = salesforce.models.BooleanField(
        db_column="Week_Reminder_Sent__c",
    )
    day_reminder_sent = salesforce.models.BooleanField(
        db_column="Day_Reminder_Sent__c",
    )

    class Meta:
        db_table="Meeting_Order__c"
        managed=True
    
    def __str__(self):
        return f"{self.mentor.full_name} | {self.meeting.meeting_type.title}"

    def is_checked_in(self):
        return self.check_in is not None

    is_checked_in.boolean = True
