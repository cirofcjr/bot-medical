from django.db import models


# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=50)
    crm = models.CharField(max_length=50)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

class Cliente(models.Model):
    nome = models.CharField(max_length=50)

class Convenio(models.Model):
    nome = models.CharField(max_length=50)

class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
