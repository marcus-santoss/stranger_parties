from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from stranger_parties.core.mixins import (
    DefaultMixin,
    IntegrityProtectedCreateMixin,
    ProtectedDestroyMixin,
)
from stranger_parties.invite.api.serializers import (
    GuestSerializer,
    EventSerializer,
    InviteDetailSerializer,
    InviteSerializer,
    EventDetailSerializer,
    GuestDetailSerializer,
)
from stranger_parties.invite.models import Guest, Event, Invite


# =====================[ GUEST ]=======================================
class GuestViewSet(
    DefaultMixin, IntegrityProtectedCreateMixin, ProtectedDestroyMixin, ModelViewSet
):
    queryset = Guest.objects.all()
    default_serializer = GuestSerializer
    search_fields = ["email"]
    serializers = {"retrieve": GuestDetailSerializer}


# =====================[ EVENT ]=======================================
class EventViewSet(
    DefaultMixin, IntegrityProtectedCreateMixin, ProtectedDestroyMixin, ModelViewSet
):
    queryset = Event.objects.all()
    default_serializer = EventSerializer
    search_fields = ["name"]

    serializers = {"retrieve": EventDetailSerializer}


# =====================[ INVITE ]======================================
class InviteViewSet(
    DefaultMixin, IntegrityProtectedCreateMixin, ProtectedDestroyMixin, ModelViewSet
):
    queryset = Invite.objects.all()
    default_serializer = InviteDetailSerializer
    filterset_fields = ["guest", "event"]

    serializers = {"create": InviteSerializer}


# =====================[ ACCEPT INVITE ]======================================
class AcceptInvite(APIView):
    def get(self, request, *args, **kwargs):
        key = request.query_params.get("key", None) or None
        if key is None:
            raise ValidationError({"key": "Invite key is required"})

        invite = Invite.objects.filter(key=key)
        if not invite.exists():
            raise ValidationError(
                {"invite": f"Invitation with key {key} was not found in the system"}
            )

        invite = invite.first()
        if not invite.is_expired:
            if not invite.confirmed:
                invite.confirmed = True
                invite.save()
                return Response(
                    {"detail": "Convite confirmado com sucesso."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Este convite já foi confirmado."},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"detail": "Este convite está expirado."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
