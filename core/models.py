from django.db import models
import datetime
from django.core.exceptions import ValidationError

# Create your models here.


class Especialidade(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, verbose_name='Descrição')

    def __str__(self):
        return self.nome


def convert(horas, minutos, segundos):
    return datetime.timedelta(hours=horas, minutes=minutos, seconds=segundos)


class Turno(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()
    nome = models.CharField(max_length=50, null=True)
    dia_agenda = models.ForeignKey('core.DiaAgenda', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):

        horario1 = convert(
            self.inicio.hour, self.inicio.minute, self.inicio.second)
        horario2 = convert(self.fim.hour, self.fim.minute, self.fim.second)
        qtd_de_horas = horario2 - horario1
        tempo_consulta = datetime.timedelta(seconds=1800)

        qtd_de_escalas = qtd_de_horas / tempo_consulta

        inicio = horario1
        fim = horario1 + tempo_consulta
        super(Turno, self).save(*args, **kwargs)
        for i in range(int(qtd_de_escalas)):
            if self.tempo.filter(inicio=str(inicio)).count() == 0:
                escala = EscalaTempo.objects.create(
                    inicio=str(inicio), fim=str(fim), turno=self)
                inicio = fim
                fim = inicio + tempo_consulta
            else:
                inicio = fim
                fim = inicio + tempo_consulta


class EscalaTempo(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()
    turno = models.ForeignKey(
        Turno, related_name="tempo", on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)


class Medico(models.Model):
    nome = models.CharField(max_length=50)
    crm = models.CharField(max_length=50)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class DiaAgenda(models.Model):
    data = models.DateField()
    # turnos = models.ForeignKey(Turno, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)


class Cliente(models.Model):

    SEXO_CHOICES = (
        ('M', u'Masculino'),
        ('F', u'Feminino'),
    )

    nome = models.CharField(max_length=50)
    cpf = models.CharField(
        max_length=11, verbose_name='Nº CPF', blank=True, null=True)
    telefone = models.CharField(
        max_length=11, verbose_name='Nº Telefone', blank=True, null=True)
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name='Data de nascimento')
    sexo = models.CharField(max_length=1, null=True, choices=SEXO_CHOICES)
    convenio = models.ForeignKey('core.Convenio', on_delete=models.CASCADE)


    def __str__(self):
        return self.nome


class Convenio(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    data = models.DateField(null=True)
    inicio = models.TimeField(null=True)
    fim = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.medico.nome + " " + self.cliente.nome

    def clean(self):
        super(Consulta, self).clean()
        data_informada = self.medico.diaagenda_set.filter(data=self.data)
        if data_informada.count() == 0:
            raise ValidationError(
                'O medico escolhido não tem agenda disponivel para esse dia')
        else:
            turnos = data_informada[0].turno_set.filter(tempo__inicio=self.inicio,
                                                     tempo__disponivel=True)
            print(turnos)
            if turnos.count() == 0:
                raise ValidationError('O horário não está disponivel')

        # if self.nome == '':
        #     raise ValidationError('Proibido criar disciplina sem nome')

    def save(self, *args, **kwargs):
        self.full_clean()

        data_informada = self.medico.diaagenda_set.filter(data=self.data)
        if data_informada.count() != 0:
            turno = data_informada[0].turno_set.filter(tempo__inicio=self.inicio,
                                                    tempo__disponivel=True)
            if turno.count() == 1:
                escala = turno[0].tempo.filter(inicio=self.inicio)
                escala = escala[0]
                escala.disponivel = False
                escala.save()
                self.fim = escala.fim

                super(Consulta, self).save(*args, **kwargs)
