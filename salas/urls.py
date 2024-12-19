from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sala/<int:sala_id>/calendario/', views.calendario_sala, name='calendario_sala'),
    path('atualizar-status-salas/', views.atualizar_status_salas, name='atualizar_status_salas'),
]