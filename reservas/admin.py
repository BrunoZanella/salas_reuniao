from django.contrib import admin
from .models import Reserva, ConfiguracaoSistema

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'data', 'hora_inicio', 'hora_fim', 'usuario')
    search_fields = ('sala__nome', 'usuario__nome')

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('limite_reservas_por_usuario',)
