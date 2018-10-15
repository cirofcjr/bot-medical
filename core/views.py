from django.shortcuts import render
from .models import Medico, Especialidade, Cliente, Consulta, Convenio


# Create your views here.
def index(request):
    template_name = 'index.html'
    context = {
        "medicos": Medico.objects.all(),
        "especialidades": Especialidade.objects.all(),
        "cliente": Cliente.objects.all(),
        "consulta": Consulta.objects.all(),
        "convenio": Convenio.objects.all(),

    }
    return render(request, template_name, context)
