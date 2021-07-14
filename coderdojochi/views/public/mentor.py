from django.views.generic import DetailView, ListView

from ...models import CDCUser


class MentorListView(ListView):
    model = CDCUser

    def get_queryset(self):
        return (
            CDCUser.objects.filter(
                user__is_active=True,
                is_active=True,
                is_public=True,
                background_check=True,
                avatar_approved=True,
                role="mentor"
            )
            .select_related("user")
            .order_by("user__date_joined")
        )


class MentorDetailView(DetailView):
    model = CDCUser

    def get_queryset(self):
        return CDCUser.objects.filter(
            user__is_active=True,
            is_active=True,
            is_public=True,
            background_check=True,
            avatar_approved=True,
            role="mentor"
        ).select_related("user")
