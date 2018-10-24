from rest_framework import serializers
from .models import Especialidade, Medico, DiaAgenda, Turno, EscalaTempo, Cliente, Convenio, Consulta

class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = ('id','nome','descricao')

class ConveniosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Convenio
        fields = ('id','nome',)


class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta
        fields =('medico','cliente','data','inicio')



class ClienteSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Cliente
        fields = ('id','nome','cpf','telefone','data_nascimento','sexo','convenio')


class EscalaTempoSerializer(serializers.ModelSerializer):


    class Meta:
        model = EscalaTempo
        fields = ('inicio', 'fim', 'disponivel',)


class TurnoSerializer(serializers.ModelSerializer):
    escalas = EscalaTempoSerializer(source='tempo', many=True)

    class Meta:
        model = Turno
        fields = ('id','inicio', 'fim', 'escalas')


class DiaAgendaSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format="%d/%m/%Y")
    turnos = TurnoSerializer(many=True, read_only=True, source='turno_set')

    class Meta:
        model = DiaAgenda
        fields = ('pk','data', 'turnos', 'medico')

class DiaAgendaSerializerEspecialidade(serializers.ModelSerializer):
    data = serializers.DateField(format="%d/%m/%Y")
    turno__tempo__inicio = serializers.TimeField()
    medico__nome = serializers.CharField()
    medico__pk = serializers.CharField()

    class Meta:
        model = DiaAgenda
        fields = ('pk','data','turno__tempo__inicio','medico__nome','medico__pk')


class MedicoSerializer(serializers.ModelSerializer):
    agenda = DiaAgendaSerializer(source='diaagenda_set', many=True, read_only=True)

    class Meta:
        model = Medico
        fields = ('pk','nome', 'crm', 'agenda','especialidade')
