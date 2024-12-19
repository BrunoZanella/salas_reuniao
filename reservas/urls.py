from django.urls import path
from . import views

urlpatterns = [
    path('criar/<int:sala_id>/', views.criar_reserva, name='criar_reserva'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('editar/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('excluir/<int:reserva_id>/', views.excluir_reserva, name='excluir_reserva'),
    path('verificar-disponibilidade/<int:sala_id>/<str:data>/<str:hora_inicio>/', 
         views.verificar_disponibilidade, name='verificar_disponibilidade'),
    path('relatorio/', views.relatorio_reservas, name='relatorio_reservas'),
    path('api/proxima-semana/<str:data>/', views.proxima_semana, name='proxima_semana'),
    path('api/semana-anterior/<str:data>/', views.semana_anterior, name='semana_anterior'),
]