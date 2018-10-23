from taiga.urls import *
urlpatterns += [
    url(r"^api/oidc/", include("mozilla_django_oidc.urls")),
]
