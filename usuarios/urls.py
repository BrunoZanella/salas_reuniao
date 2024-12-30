from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', views.user_logout, name='logout'),

    # URLs para redefinição de senha
    path('redefinir-senha/', 
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/password_reset.html',
             email_template_name='usuarios/password_reset_email.html',
             subject_template_name='usuarios/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('redefinir-senha/enviado/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('redefinir-senha/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('redefinir-senha/concluido/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
