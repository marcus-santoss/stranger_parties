from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt import authentication


class DefaultMixin:
    serializers = dict()
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
