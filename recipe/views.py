from rest_framework.views import APIView
from rest_framework.response import Response 
from django.http import JsonResponse
from rest_framework import permissions, status
from .serializers import RecipeSerializer
from  .models import Recipe
import jwt, datetime, bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from users.models import User

class CreateRecipeView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    @extend_schema(
        request=OpenApiTypes.OBJECT, 
        examples=[
            OpenApiExample(
                "Create Recipe",
                value={
                    "name": "Pasta",
                    "description": "A cool recipe for pasta",
                    "ingredients": {"spice", "tomatoes"},
                }
            )
        ],
        tags=["Recipes"]
    )
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        name = request.data['name']
        
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            recipe = serializer.save(user=user)
            return Response({ "message": "Recipe Created Successfully", "date": RecipeSerializer(recipe).data, "status": status.HTTP_201_CREATED})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveRecipeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)  

    @extend_schema(
        tags=["Recipes"]
    )
    def get(self, request, id):
        user = User.objects.get(id=request.user.id)
        try:
            recipe = Recipe.objects.get(id=id, user=user) 
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecipeSerializer(recipe)
        return Response({"data": serializer.data})

class ListUserRecipesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(
        tags=["Recipes"]
    )
    def get(self, request):
        recipes = Recipe.objects.filter(user=request.user.id)  
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

class DeleteRecipeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    @extend_schema(
        tags=["Recipes"]
    )
    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id, user=request.user.id)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)  
            
        recipe.delete()
        return Response({"message": "Recipe Deleted", "status": status.HTTP_204_NO_CONTENT})

class UpdateRecipeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=OpenApiTypes.OBJECT, 
        examples=[
            OpenApiExample(
                "Edit Recipe",
                value={
                    "ingredients": {"spice", "tomatoes"},
                }
            )
        ],        
        tags=["Recipes"]
    )    
    def put(self, request, id):
        user = User.objects.get(id=request.user.id)
        try:
            recipe = Recipe.objects.get(id=id, user=user)    
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)  
            
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({ "message": "Recipe Updated Successfully", "data":serializer.data})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
