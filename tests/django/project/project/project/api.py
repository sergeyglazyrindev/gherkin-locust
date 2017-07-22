from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.response import Response


class BuildViewSet(
        viewsets.ViewSet
):
    permission_classes = (AllowAny, )

    def list(self, *args, **kwargs):
        return Response({'dsadas': 1})
