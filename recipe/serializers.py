from rest_framework import serializers
from .models import Recipe
from users.serializers import UserSerializer 


class RecipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients', 'user']
        