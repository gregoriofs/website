# from django.db import models

from .common import CommonInfo

import salesforce

class EquipmentType(salesforce.models.SalesforceModel):
# class EquipmentType(CommonInfo):

    name = salesforce.models.CharField(
        max_length=255,
        blank=False,
        null=False,
        db_column="Name__c"
    )
    
    class Meta:
        db_table="Equipment_Type__c"
        managed=True

    def __str__(self):
        return self.name


class Equipment(salesforce.models.SalesforceModel):
    # class Equipment(CommonInfo):
    WORKING = "working"
    ISSUE = "issue"
    UNUSABLE = "unusable"
    EQUIPMENT_CONDITIONS = [
        (WORKING, "Working"),
        (ISSUE, "Issue"),
        (UNUSABLE, "Unusable"),
    ]

    uuid = salesforce.models.CharField(
        max_length=255,
        verbose_name="UUID",
        default="000-000-000-000",
        null=False,
        db_column="uuid__c"
    )

    equipment_type = salesforce.models.ForeignKey(
        EquipmentType,
        on_delete=salesforce.models.DO_NOTHING,
        db_column="Type__c"
    )

    make = salesforce.models.CharField(
        max_length=255,
        db_column="Make__c"
    )

    model = salesforce.models.CharField(
        max_length=255,
        db_column="Model__c"
    )

    asset_tag = salesforce.models.CharField(
        max_length=255,
        db_column="Asset_Tag__c"
    )

    acquisition_date = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        db_column="Acquisition_Date__c"
    )

    condition = salesforce.models.CharField(
        max_length=255,
        choices=EQUIPMENT_CONDITIONS,
        db_column="Condition__c"
    )

    notes = salesforce.models.TextField(
        blank=True,
        null=True,
        db_column="Notes__c"
    )

    last_system_update_check_in = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Check In",
        db_column="Last_System_Update_Check__c"
    )

    last_system_update = salesforce.models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Update",
        db_column="Last_System_Update__c"
    )

    force_update_on_next_boot = salesforce.models.BooleanField(
        default=False,
        verbose_name="Force Update",
        db_column="Force_Update_Next__c"
    )

    class Meta:
        verbose_name = "equipment"
        verbose_name_plural = "equipment"
        db_table="Equipment__c"
        managed=True

    def __str__(self):
        return f"{self.equipment_type.name} | {self.make} {self.model} | {self.acquisition_date}"
