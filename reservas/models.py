from django.db import models
from django.conf import settings
from salas.models import Sala

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nome_nao_registrado = models.CharField(max_length=100, null=True, blank=True)
    empresa_nao_registrado = models.CharField(max_length=100, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['data', 'hora_inicio']
        
    def __str__(self):
        nome = self.usuario.nome if self.usuario else self.nome_nao_registrado
        return f"{self.sala.nome} - {self.data} {self.hora_inicio} - {nome}"
    
    def get_nome_usuario(self):
        if self.usuario:
            return f"{self.usuario.nome} {self.usuario.sobrenome}"
        return self.nome_nao_registrado
    
    def get_empresa(self):
        if self.usuario:
            return self.usuario.empresa
        return self.empresa_nao_registrado

    def display_usuario(self):
        """Retorna o nome do usuário ou o nome não registrado."""
        if self.usuario:
            return self.usuario.nome
        return self.nome_nao_registrado
    display_usuario.short_description = 'Usuário'