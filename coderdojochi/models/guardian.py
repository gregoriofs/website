# from django.db import models

from .common import CommonInfo
from .race_ethnicity import RaceEthnicity
from .user import CDCUser
import salesforce

class Guardian(salesforce.models.SalesforceModel):
    # class Guardian(CommonInfo)

    HISPANIC = "Hispanic"
    NOT_HISPANIC = "Not Hispanic"

    ETHNICITY = [
        (HISPANIC,"Hispanic"),
        (NOT_HISPANIC,"Not Hispanic"),
    ]

    user = salesforce.models.ForeignKey(
        CDCUser,
        on_delete=salesforce.models.PROTECT,
    )
    is_active = salesforce.models.BooleanField(
        db_column="Active__c",
        
    )
    phone = salesforce.models.CharField(
        db_column="Phone",
        max_length=50,
        blank=True,
    )
    #what is zip
    # address = salesforce.models.Fore(
    #     max_length=20,
    #     blank=True,
    #     null=True,
    # )
    birthday = salesforce.models.DateField(
        db_column="Birthdate",
        blank=False,
        null=True,
    )
    gender = salesforce.models.CharField(
        db_column="Gender__c",
        max_length=255,
        blank=False,
        null=True,
    )
    #race_ethnicity = models.ManyToManyField(
    #     RaceEthnicity,
    #     blank=False,
    # )
    
    ethnicity = salesforce.models.CharField(
        choices=ETHNICITY,
        max_length=255,
        db_column="hed__Ethnicity__c",
        default=""
    )
    race = salesforce.models.CharField(
        max_length=255,
        db_column="hed__Race__c",
        default=""
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "Contact"
        managed=True

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def email(self):
        return self.user.email

    def get_students(self):
        from .student import Student

        return Student.objects.filter(
            guardian=self,
            is_active=True,
        )
