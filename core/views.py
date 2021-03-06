from django.shortcuts import render
from .models import Medico, Especialidade, Cliente, Consulta, Convenio, Turno, Medico, DiaAgenda, EscalaTempo
from rest_framework import generics
from .serializers import EspecialidadeSerializer, ConsultaSerializer, ConveniosSerializer, ClienteSerializer, EscalaTempoSerializer, MedicoSerializer, DiaAgendaSerializer, DiaAgendaSerializerEspecialidade
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime
from django_filters import rest_framework as filters
import json
from core.regex import validacao_do_cpf

# Create your views here.


@api_view(['GET', 'POST'])
def webhook(request):

    dates = {"fulfillmentText": "Ola tudo bem"}
    date2 = ""

    def dates2(value):
        date2 = {
            "fulfillmentMessages": [
                # {

                #         "card": {
                #             "title": "card title",
                #             "subtitle": "card text",
                #             "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                #             "buttons": [
                #                 {
                #                     "text": "button text",
                #                     "postback": "https://assistant.google.com/"
                #                 }
                #             ]
                #         }

                # }
                {
                    "text": {
                        "text": [value]
                    },


                }
            ]

        }
        # date2 = {"fulfillmentText": value + "\n\n teste" + "/n/n teste"}

        return date2

    def consulta_paciente(self, cpf):
        cpf = validacao_cpf(entrada['cpf'])
        query = Cliente.objects.filter(cpf=cpf)
        if query.count() > 0:
            cliente = query[0]
        r = Response(
            dates2(cliente.nome),)
        r.content_type = 'application/json; charset=UTF-8'
        print(r.content_type)
        return r

    if request.method == 'POST':
        # converte os dados recebidos do body em formato json
        json_data = json.loads(str(request.body, encoding='utf-8'))

        # intent
        intent_name = json_data['queryResult']['intent']['displayName']
        print(intent_name)
        # esses são os parametros que solicitei do usuario
        entrada = json_data['queryResult']['parameters']
        # consulta o banco de dados e verifica se existe alguem com o cpf digitado e se houver
        # ele retorna nome e cpf
        if intent_name == "consulta.paciente":
            cpf = validacao_do_cpf(entrada['cpf'])
            query = Cliente.objects.filter(cpf=cpf)
            if query.count() > 0:
                cliente = query[0]

                r = Response(
                    dates2("Olá, " + cliente.nome + ".\nVamos agendar? "),)
                r.content_type = 'application/json; charset=UTF-8'
                return r
            else:
                r = Response(
                    {
                        "followupEventInput": {
                            "name": "usuario_nao_cadastrado"
                        }
                    }
                )
                r.content_type = 'application/json; charset=UTF-8'
                return r

        if intent_name == "consulta.paciente - yes":
            print("entrei")
            r = Response(
                dates2("Qual a especialidade você deseja agendar a consulta ?"))
            r.content_type = 'application/json; charset=UTF-8'
            return r

        date2 = dates2("intent diferente")

        return Response(date2)
    return Response(date2)


def index(request):
    template_name = 'index.html'
    context = {
        "medicos": Medico.objects.all(),
        "especialidades": Especialidade.objects.all(),
        "cliente": Cliente.objects.all(),
        "consulta": Consulta.objects.all(),
        "convenio": Convenio.objects.all(),
        "turnos": Turno.objects.all(),

    }
    return render(request, template_name, context)


class list_especialidades(generics.ListCreateAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    name = 'list-especialidades'


class list_consultas(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    name = 'list-consultas'


class medicos_especialidade(generics.ListCreateAPIView):
    serializer_class = MedicoSerializer
    name = 'medico-especialidades'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Medico.objects.filter(especialidade__pk=pk)
        return queryset


class especialidade_detail(generics.RetrieveDestroyAPIView):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer
    name = 'especialidade-detail'

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        especialidade = Especialidade.objects.get(pk=pk)
        especialidade.delete()
        if Especialidade.objects.filter(pk=pk).exists() == False:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'mensagem': 'Deletado com sucesso'})
        # else:
            # return Response(status=status.HTTP_204_NO_CONTENT)


class list_medico(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    name = 'list-medico'


class list_cliente(generics.ListCreateAPIView):
    filter_fields = ('cpf',)
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    name = 'list-client'


class cliente_detail(generics.RetrieveDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    name = 'medico-detail'


class escalas_medico(generics.ListCreateAPIView):
    serializer_class = DiaAgendaSerializer
    name = 'custom'
    filter_fields = ('data',)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        medico = Medico.objects.filter(pk=int(pk))
        medico = medico[0]
        queryset = medico.diaagenda_set.all()
        data = self.request.query_params.get('data', None)
        if data is not None:
            print('pronto')
        return queryset


class list_convenio(generics.ListCreateAPIView):
    # filter_fields = ('cpf',)
    queryset = Convenio.objects.all()
    serializer_class = ConveniosSerializer
    name = 'list-convenio'


class especialidade_data(generics.ListCreateAPIView):
    serializer_class = DiaAgendaSerializerEspecialidade
    name = 'dados'
    filter_fields = ('data',)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        hoje = datetime.date.today()
        medico = DiaAgenda.objects.filter(data__gte=hoje, medico__especialidade__pk=pk, turno__tempo__disponivel=True).values(
            'data', 'turno__tempo__inicio', 'medico__nome', 'medico__pk').distinct()
        print(medico)
        return medico


class medico_detail(generics.RetrieveDestroyAPIView):
    queryset = Medico.objects.all()
    filter_fields = ('nome',)
    serializer_class = MedicoSerializer
    name = 'medico-detail'

    def get_queryset(self):

        queryset = Medico.objects.all()
        favorite = self.kwargs.get('pk')
        print(favorite)

        data = self.request.query_params.get('data', None)
        if data is not None:
            print('pronto')
        return queryset
