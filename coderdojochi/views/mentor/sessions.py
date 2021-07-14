from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from ...models import MentorOrder, Session, CDCUser
#Removed Mentor from Models

class SessionDetailView(DetailView):
    model = Session
    template_name = "mentor/session_detail.html"

    def get_context_data(self, **kwargs):
        session = self.object
        mentor = get_object_or_404(CDCUser, user=self.request.user,role="mentor")

        session_orders = MentorOrder.objects.filter(
            session=session,
            is_active=True,
        )

        context = super().get_context_data(**kwargs)
        context["mentor_signed_up"] = session_orders.filter(mentor=mentor).exists()
        context["spots_remaining"] = session.mentor_capacity - session_orders.count()
        context["account"] = mentor

        context["active_mentors"] = CDCUser.objects.filter(
            role="mentor",
            id__in=MentorOrder.objects.filter(
                session=self.object,
                is_active=True,
            ).values("mentor__id")
        )

        return context
