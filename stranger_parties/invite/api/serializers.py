import uuid

from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer, ListSerializer

from stranger_parties.invite.models import Guest, Event, Invite


# ==================[ GUEST ]=============================================
class GuestSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "email", "name", "phone"]


# ==================[ EVENT ]=============================================
class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date_time"]


class InviteEventOnlySerializer(ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Invite
        fields = ["event", "confirmation_link"]


class GuestDetailSerializer(ModelSerializer):
    total_invites = IntegerField()
    attended_events = InviteEventOnlySerializer(many=True)
    pendent_events = InviteEventOnlySerializer(many=True)

    class Meta:
        model = Guest
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "total_invites",
            "attended_events",
            "pendent_events",
        ]


class InviteGuestOnlySerializer(ModelSerializer):
    guest = GuestSerializer()

    class Meta:
        model = Invite
        fields = ["guest"]


class EventDetailSerializer(ModelSerializer):
    confirmed_guests = InviteGuestOnlySerializer(many=True)
    non_confirmed_guests = InviteGuestOnlySerializer(many=True)
    total_invited = IntegerField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date_time",
            "total_invited",
            "confirmed_guests",
            "non_confirmed_guests",
        ]


# ==================[ INVITE ]============================================


class InviteSerializer(ModelSerializer):
    guest = ListSerializer(child=IntegerField(), required=True, write_only=True)

    def to_representation(self, instance):
        event = instance.event
        return {
            "message": "All users are invited to event",
            "event_name": event.name,
            "event_date": event.date_time.strftime("%d/%m/%Y %H:%M"),
            "total_invited": event.total_invited,
        }

    def create(self, validated_data):
        guest_list = validated_data.pop("guest")
        validated_data["guest_id"] = guest_list.pop(0)
        invite = super(InviteSerializer, self).create(validated_data)

        for pk in guest_list:
            invite.pk = None
            invite.key = uuid.uuid4()
            invite.guest_id = pk
            invite.save()

        return invite

    class Meta:
        model = Invite
        fields = ["guest", "event"]
        extra_kwargs = {"event": {"write_only": True}}


class InviteDetailSerializer(ModelSerializer):
    guest = GuestSerializer()
    event = EventSerializer()

    class Meta:
        model = Invite
        fields = [
            "id",
            "key",
            "confirmed",
            "guest",
            "event",
            "sent_date",
            "confirmation_link",
            "is_expired",
            "guest",
            "event",
        ]
