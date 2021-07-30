import environ
from django.urls import path, re_path, include
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken

from stranger_parties.invite import urls
from stranger_parties.router import router

env = environ.Env()
environ.Env.read_env()

open_api_obj = openapi.Info(
    title="Stranger Parties API",
    default_version="v1",
    description="Rest API for the system Strainger Parties",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="marcuspnascimento@gmail.com"),
    license=openapi.License(name="BSD License"),
)
schema_view = get_schema_view(
    open_api_obj,
    public=True,
    authentication_classes=(JSONWebTokenAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("api/", include(router.urls)),
    path("api/", include("stranger_parties.invite.urls")),
    path("api/auth/", ObtainJSONWebToken.as_view()),
    re_path(
        r'^schema(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
]
