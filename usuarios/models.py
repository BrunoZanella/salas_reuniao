from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    empresa = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.first_name = self.nome
        self.last_name = self.sobrenome
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.nome and self.sobrenome:
            return f"{self.nome} {self.sobrenome}"
        return self.username