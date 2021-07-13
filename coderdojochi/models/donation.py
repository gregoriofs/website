from django.contrib.contenttypes.models import ContentType
# from django.db import models
from django.urls import reverse

from .common import CommonInfo

import salesforce

class Donation(salesforce.models.SalesforceModel):
    # class Donation(CommonInfo):
    from .session import Session
    from .user import CDCUser

    user = salesforce.models.ForeignKey(
        CDCUser,
        blank=True,
        null=True,
        on_delete=salesforce.models.DO_NOTHING,
    )
    session = salesforce.models.ForeignKey(
        Session,
        blank=True,
        null=True,
        on_delete=salesforce.models.DO_NOTHING,
        db_column="Course_Offering__c",
    )
    first_name = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="First_Name__c"
    )
    last_name = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Last_Name__c"
    )
    referral_code = salesforce.models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_column="Referral_Code__c"
    )
    email = salesforce.models.EmailField(
        blank=True,
        null=True,
        db_column="Email__c"
    )
    amount = salesforce.models.IntegerField()
    is_verified = salesforce.models.BooleanField(
        db_column="Is_Verified__c",
    )
    receipt_sent = salesforce.models.BooleanField(
        db_column="Receipt_Sent__c",
    )

    def __str__(self):
        return f"{self.email} | ${self.amount}"

    class Meta:
        db_table="Donation__c"
        managed=True
        
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            f"admin:{content_type.app_label}_{content_type.model}_change",
            args=(self.id,),
        )

    def get_first_name(self):
        if self.user:
            return self.user.first_name
        else:
            return self.first_name

    get_first_name.short_description = "First Name"

    def get_last_name(self):
        if self.user:
            return self.user.last_name
        else:
            return self.last_name

    get_last_name.short_description = "Last Name"

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.email

    get_email.short_description = "Email"
