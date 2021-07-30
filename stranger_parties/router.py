from rest_framework import routers

from stranger_parties.invite.api.router import invite_router

router = routers.DefaultRouter()

# INVITE
router.registry.extend(invite_router.registry)
