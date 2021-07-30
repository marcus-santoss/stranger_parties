from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from stranger_parties.invite.models import Guest, Event, Invite


# ==================[ EVENT ]=============================================
class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date_time"]


# ==================[ GUEST ]=============================================
class GuestSerializer(ModelSerializer):
    def create(self, validated_data):
        user = super(GuestSerializer, self).create(validated_data)
        enc_password = make_password(user.password)
        user.password = enc_password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = None

        if "password" in validated_data.keys():
            password = validated_data.pop("password")

        user = super(GuestSerializer, self).update(instance, validated_data)

        if password is not None:
            user.password = make_password(password)
            user.save()

        return user

    class Meta:
        model = Guest
        fields = ["id", "email", "first_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class GuestDetailSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "email", "first_name", "last_name", "is_active", "last_login"]
        read_only_fields = ["id", "is_active"]


# ==================[ INVITE ]============================================
class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = ["guest", "event"]


class InviteDetailSerializer(ModelSerializer):
    guest = GuestDetailSerializer()
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
            "link",
            "is_expired",
            "guest",
            "event",
        ]
