from rest_framework import routers
from .project.api import BuildViewSet
from .users.api import (
    UserViewSet,
    LoginViewSet
)

# Routers provide an easy way
# of automatically determining
# the URL conf.
router = routers.DefaultRouter()
core_endpoints = (
    (
        'users',
        UserViewSet,
        'users'
    ),
    (
        'login',
        LoginViewSet,
        'login'
    ),
)

cached_endpoints = (
    (
        'build',
        BuildViewSet,
        'build'
    ),
)
for endpoint in core_endpoints:
    base_name = None
    try:
        if endpoint[2]:
            base_name = endpoint[2]
    except IndexError:
        pass
    router.register(
        r'core/' + endpoint[0],
        endpoint[1],
        base_name
    )

for endpoint in cached_endpoints:
    base_name = None
    try:
        if endpoint[2]:
            base_name = endpoint[2]
    except IndexError:
        pass
    router.register(
        r'cached/' + endpoint[0],
        endpoint[1],
        base_name
    )
