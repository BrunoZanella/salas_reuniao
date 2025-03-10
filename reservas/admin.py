from django.contrib import admin
from .models import Reserva, ConfiguracaoSistema, ContatoWhatsApp

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'data', 'hora_inicio', 'hora_fim', 'usuario')
    search_fields = ('sala__nome', 'usuario__nome')


class ContatoWhatsAppInline(admin.TabularInline):
    model = ContatoWhatsApp
    extra = 1  # Quantidade de campos extras para adicionar novos contatos

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('limite_reservas_por_usuario',)
    inlines = [ContatoWhatsAppInline]

