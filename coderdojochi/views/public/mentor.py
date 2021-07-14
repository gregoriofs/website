from coderdojochi.models.user import CDCUser
from django.views.generic import DetailView, ListView

from django.contrib.auth import get_user_model

User = get_user_model()


class MentorListView(ListView):
    model = CDCUser

    def get_queryset(self):
        return (
            User.objects.filter(
                user__is_active=True,
                is_active=True,
                is_public=True,
                background_check=True,
                avatar_approved=True,
                role=CDCUser.MENTOR,
            )
            .select_related("user")
            .order_by("user__date_joined")
        )


class MentorDetailView(DetailView):
    model = CDCUser

    def get_queryset(self):
        return User.objects.filter(
            user__is_active=True,
            is_active=True,
            is_public=True,
            background_check=True,
            avatar_approved=True,
            roel = CDCUser.MENTOR,
        ).select_related("user")
