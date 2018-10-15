from django.db import models


# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=50)


class Medico(models.Model):
    nome = models.CharField(max_length=50)
    crm = models.CharField(max_length=50)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
