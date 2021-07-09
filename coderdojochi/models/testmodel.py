from django.db import models

import salesforce


class TestModel(salesforce.models.SalesforceModel):
    Name = salesforce.models.CharField(
        max_length = 255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.Name}"

    class Meta:
        db_table = "Test_Model__c"
        managed = True


class HelloWorldModel(salesforce.models.SalesforceModel):
    test= salesforce.models.ForeignKey(TestModel,related_name='Test_Model__c', db_column="Test__c",on_delete=models.DO_NOTHING, custom=True)
    body = salesforce.models.TextField(db_column="Body__c")

    class Meta:
        db_table = "Hello_World_Model__c"
        managed = True
