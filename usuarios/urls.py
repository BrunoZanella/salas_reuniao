from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', views.user_logout, name='logout'),
]