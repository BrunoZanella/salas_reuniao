from django.contrib import admin
from .models import Reserva


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('display_usuario','sala','data','hora_inicio','hora_fim')
    
admin.site.register(Reserva, ReservaAdmin)

