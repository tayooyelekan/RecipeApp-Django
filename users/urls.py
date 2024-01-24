from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('edit', views.EditUserView.as_view(), name='edit'),
    path('get', views.UserView.as_view(), name='get'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('delete', views.DeleteUserView.as_view(), name='delete'),
    path('getall', views.ListUsersView.as_view(), name='getall'),
    path('changepassword', views.ChangePasswordView.as_view(), name='changepassword')
]