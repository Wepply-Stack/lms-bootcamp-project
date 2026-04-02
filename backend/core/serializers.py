from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta(object):
        model = User
        fields = ['id', 'email', 'role']

    def get_role(self,obj):
        return "admin" if obj.is_staff else "employee"

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)