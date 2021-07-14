from coderdojochi.models.user import CDCUser
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from ...models import MentorOrder, Session
from django.contrib.auth import get_user_model
User = get_user_model()

class SessionDetailView(DetailView):
    model = Session
    template_name = "mentor/session_detail.html"

    def get_context_data(self, **kwargs):
        session = self.object
        mentor = get_object_or_404(User, user=self.request.user, role=CDCUser.MENTOR)

        session_orders = MentorOrder.objects.filter(
            session=session,
            is_active=True,
        )

        context = super().get_context_data(**kwargs)
        context["mentor_signed_up"] = session_orders.filter(mentor=mentor).exists()
        context["spots_remaining"] = session.mentor_capacity - session_orders.count()
        context["account"] = mentor

        context["active_mentors"] = User.objects.filter(
            role=CDCUser.MENTOR,
            id__in=MentorOrder.objects.filter(
                session=self.object,
                is_active=True,
            ).values("mentor__id")
        )

        return context
