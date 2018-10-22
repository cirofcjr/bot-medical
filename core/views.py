from django.shortcuts import render
from .models import Medico, Especialidade, Cliente, Consulta, Convenio, Turno, Medico, DiaAgenda
from rest_framework import generics
from .serializers import EspecialidadeSerializer, MedicoSerializer, DiaAgendaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


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


class list_medico(generics.ListCreateAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    name = 'list-medico'


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
