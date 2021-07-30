from django.urls import path

from stranger_parties.invite.api.views import AcceptInvite

app_name = "invite"
urlpatterns = [path("invite-accept/", AcceptInvite.as_view())]
