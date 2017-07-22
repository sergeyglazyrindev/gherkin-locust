from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'last_name', 'first_name', 'id', 'username']
        read_only_fields = ('id', )

    def save(self, **kwargs):
        inst = super(UserSerializer, self).save()
        inst.set_password('123456')
        inst.save()
        return inst
