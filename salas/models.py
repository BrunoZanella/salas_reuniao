from django.db import models
from datetime import datetime

class Sala(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='salas/', default='salas/logo.png')  # Definindo imagem padrão
    tamanho = models.CharField(max_length=50)
    capacidade = models.IntegerField()
    
    def __str__(self):
        return self.nome
        
    def esta_ocupada(self, data, hora_inicio, hora_fim, reserva_id=None):
        from reservas.models import Reserva
        
        query = Reserva.objects.filter(
            sala=self,
            data=data,
            hora_fim__gt=hora_inicio,  # A reserva termina após o início solicitado
            hora_inicio__lt=hora_fim  # A reserva começa antes do fim solicitado
        )
        
        # Se for um processo de edição, excluímos a reserva atual da verificação
        if reserva_id:
            query = query.exclude(id=reserva_id)
        
        return query.exists()

