from django.db import models
import datetime


# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

def convert(horas, minutos, segundos):
        return datetime.timedelta(hours=horas, minutes=minutos, seconds=segundos)

class Turno(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()

    def save(self, *args, **kwargs):

        horario1 = convert(self.inicio.hour, self.inicio.minute, self.inicio.second)
        horario2 = convert(self.fim.hour, self.fim.minute, self.fim.second)
        qtd_de_horas = horario2 - horario1
        tempo_consulta = datetime.timedelta(seconds=1800)

        qtd_de_escalas = qtd_de_horas / tempo_consulta

        qtd_de_horas = qtd_de_horas.total_seconds() / 60

        inicio = horario1
        fim = horario1 + tempo_consulta
        super(Turno, self).save(*args, **kwargs)

        for i in range(int(qtd_de_escalas)):
            escala = EscalaTempo.objects.create(inicio=str(inicio), fim=str(fim), dia=self)
            inicio = fim
            fim = inicio + tempo_consulta


class EscalaTempo(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()
    dia = models.ForeignKey(Turno, related_name="tempo", on_delete=models.CASCADE)


class Medico(models.Model):
    nome = models.CharField(max_length=50)
    crm = models.CharField(max_length=50)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class DiaAgenda(models.Model):
    data = models.DateField()
    turnos = models.ManyToManyField(Turno)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)


class Cliente(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Convenio(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)

    def __str__(self):
        return self.medico.nome + " " + self.cliente.nome
