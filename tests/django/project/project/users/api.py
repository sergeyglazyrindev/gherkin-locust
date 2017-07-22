from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(
            id=self.request.user.pk
        )


class LoginViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny, )

    def create(self, request):
        username = request.data['username']
        password = request.data['password']
        u = authenticate(
            password=password, username=username
        )
        login(request, u)
        return Response({
            'id': u.id
        })
