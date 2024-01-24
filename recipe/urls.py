from django.urls import path
from . import views


urlpatterns = [
    path('create', views.CreateRecipeView.as_view(), name='create'),
    path('update/<int:id>', views.UpdateRecipeView.as_view(), name='update'),
    path('get/<int:id>', views.RetrieveRecipeView.as_view(), name='get'),
    path('getall', views.ListUserRecipesView.as_view(), name='getall'),
    path('delete/<int:id>', views.DeleteRecipeView.as_view(), name='delete')      
]