from rest_framework import serializers
from .models import Especialidade, Medico, DiaAgenda, Turno, EscalaTempo


class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = ('nome',)


class EscalaTempoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EscalaTempo
        fields = ('inicio', 'fim', 'disponivel',)


class TurnoSerializer(serializers.ModelSerializer):
    escalas = EscalaTempoSerializer(source='tempo', many=True)

    class Meta:
        model = Turno
        fields = ('inicio', 'fim', 'escalas')


class DiaAgendaSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format="%d/%m/%y")
    turnos = TurnoSerializer(many=True, read_only=True)

    class Meta:
        model = DiaAgenda
        fields = ('data', 'turnos', 'medico')


class MedicoSerializer(serializers.ModelSerializer):
    agenda = DiaAgendaSerializer(source='diaagenda_set', many=True)

    class Meta:
        model = Medico
        fields = ('nome', 'crm', 'agenda')
