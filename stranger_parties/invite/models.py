import uuid

from django.db import models
from django.utils import timezone

from stranger_parties.core.models import BaseModel, User


class Guest(BaseModel):
    name = models.CharField(null=False, max_length=80)
    email = models.EmailField(null=False, unique=True)
    phone = models.CharField(null=False, max_length=15)

    @property
    def attended_events(self):
        return self.event_invitations.filter(confirmed=True).count()

    @property
    def pendent_events(self):
        return self.event_invitations.filter(confirmed=False).count()

    @property
    def total_invites(self):
        return self.event_invitations.count()

    def __str__(self):
        return self.name


class Event(BaseModel):
    name = models.CharField(max_length=80, null=False)
    date_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Invite(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    confirmed = models.BooleanField(default=False)

    guest = models.ForeignKey(
        Guest, related_name="event_invitations", on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event, related_name="guest_invitations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Invite {self.guest.name} to {self.event.name}"

    @property
    def sent_date(self):
        return self.created_at

    @property
    def url(self):
        return "http://0.0.0.0:8000/invite-accept"

    @property
    def link(self):
        return f"{self.url}/{self.key}/"

    @property
    def is_expired(self):
        return self.event.date_time > timezone.now()

    class Meta:
        unique_together = ["guest", "event"]
