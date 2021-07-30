from rest_framework import routers

from stranger_parties.invite.api.views import GuestViewSet, EventViewSet, InviteViewSet

invite_router = routers.DefaultRouter()
invite_router.register("guest", GuestViewSet)
invite_router.register("event", EventViewSet)
invite_router.register("invite", InviteViewSet)
