from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from stranger_parties.core.mixins import DefaultMixin
from stranger_parties.invite.api.serializers import (
    GuestSerializer,
    GuestDetailSerializer,
    EventSerializer,
    InviteDetailSerializer,
    InviteSerializer,
)
from stranger_parties.invite.models import Guest, Event, Invite


# =====================[ GUEST ]=======================================
class GuestViewSet(DefaultMixin, ModelViewSet):
    queryset = Guest.objects.all()
    default_serializer = GuestDetailSerializer
    search_fields = ["email"]

    serializers = {
        "create": GuestSerializer,
    }

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(email=self.request.user.email)


# =====================[ EVENT ]=======================================
class EventViewSet(DefaultMixin, ModelViewSet):
    queryset = Event.objects.all()
    default_serializer = EventSerializer
    search_fields = ["name"]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(guest_invitations__guest__email=self.request.user.email)


# =====================[ INVITE ]======================================
class InviteViewSet(DefaultMixin, ModelViewSet):
    queryset = Invite.objects.all()
    default_serializer = InviteDetailSerializer
    filterset_fields = ["guest", "event"]

    serializers = {
        "create": InviteSerializer
    }

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(guest__email=self.request.user.email)


class AcceptInvite(APIView):
    
    def get(self, request, key, *args, **kwargs):
        invite = get_object_or_404(Invite, key)

        if not invite.is_expired:
            if not invite.confirmed:
                invite.confirmed = True
                invite.save()
                return Response({"detail": "Convite confirmado com sucesso."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Este convite já foi confirmado."},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Este convite está expirado."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
