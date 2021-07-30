from django.db import IntegrityError
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt import authentication


class DefaultMixin:
    serializers = {}
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)


class IntegrityProtectedCreateMixin:
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as iex:
            raise ValidationError(
                {"integrity": str(iex).replace('"', "'").splitlines()}
            )
        except Exception as ex:
            raise ValidationError({"error": str(ex).splitlines()})


class ProtectedDestroyMixin:
    protected_model_name = "instance"

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            raise ValidationError(
                {
                    self.protected_model_name: [
                        f"This {self.protected_model_name} is associated with a one or more "
                        "records and cannot be excluded.To perform the deletion, "
                        "you must first delete all your dependencies."
                    ]
                }
            )
