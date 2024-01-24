from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):

    fullName = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    country = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id','email', 'username', 'number', 'fullName', 'bio', 'country', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # password write only
        }
