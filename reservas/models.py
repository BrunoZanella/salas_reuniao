
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from salas.models import Sala
from datetime import timedelta
from datetime import datetime

class ConfiguracaoSistema(models.Model):
    limite_reservas_por_usuario = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"

    def __str__(self):
        return f"Limite de Reservas: {self.limite_reservas_por_usuario}"

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

    def clean(self):
        usuario = self.usuario
        limite = 5  # O limite de reservas por usuário

        # Converte a data para datetime.date, se necessário
        if isinstance(self.data, str):
            self.data = datetime.strptime(self.data, '%Y-%m-%d').date()

        # Considera todas as reservas, exceto a que está sendo editada
        reservas_ativas = Reserva.objects.filter(usuario=usuario, data__month=self.data.month, data__year=self.data.year)

        # Se a reserva já estiver salva e for uma edição, desconsidera a própria reserva
        if self.id:
            reservas_ativas = reservas_ativas.exclude(id=self.id)

        if reservas_ativas.count() >= limite:
            raise ValidationError(f"O usuário {usuario} atingiu o limite de {limite} reservas para este mês.")

    def save(self, *args, **kwargs):
        self.clean()  # Aplica as validações ao salvar
        super().save(*args, **kwargs)

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
    

'''
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

'''