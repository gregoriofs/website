# from django.db import models

from .common import CommonInfo
import salesforce

class Location(salesforce.models.SalesforceModel):
    #class Location(CommonInfo):
    name = salesforce.models.CharField(
        max_length=255,
        db_column="Address_Name__c",
    )

    address = salesforce.models.CharField(
        blank=True,
        null=True,
        max_length=255,
        db_column="hed__MailingStreet__c"
    )

    city = salesforce.models.CharField(
        blank=True,
        null=True,
        max_length=255,
        db_column="hed__MailingCity__c",
    )

    state = salesforce.models.CharField(
        blank=True,
        null=True,
        max_length=2,
        db_column="hed__MailingState__c"
    )

    zip = salesforce.models.CharField(
        blank=True,
        null=True,
        max_length=20,
        db_column="hed__MailingPostalCode__c"
    )

    is_active = salesforce.models.BooleanField(
        db_column="Active__c", 
    )

    class Meta:
        ordering = ["-id"]
        db_table="hed__Address__c"
        managed=True

    def __str__(self):
        return self.name
