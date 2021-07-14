import os

from django.contrib.auth import get_user_model
from django.db import models

from coderdojochi.models.user import CDCUser

from ..notifications import NewMentorOrderNotification
from .common import CommonInfo

User = get_user_model()


class MentorOrder(CommonInfo):

    from .session import Session

    user = models.ForeignKey(
        User,
        limit_choices_to={
            "user__role": CDCUser.MENTOR,
        },
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        default=True,
    )
    ip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    check_in = models.DateTimeField(
        blank=True,
        null=True,
    )
    affiliate = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    order_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    week_reminder_sent = models.BooleanField(
        default=False,
    )
    day_reminder_sent = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.mentor.full_name} | {self.session.course.title}"

    def is_checked_in(self):
        return self.check_in is not None

    is_checked_in.boolean = True

    def save(self, *args, **kwargs):
        num_orders = MentorOrder.objects.filter(mentor__id=self.mentor.id).count()

        if self.pk is None and num_orders == 0:
            NewMentorOrderNotification(self).send()

        super().save(*args, **kwargs)
