from django.shortcuts import render
from .models import Medico, Especialidade

# Create your views here.
def index(request):
    template_name = 'index.html'
    context = {
        "medicos": Medico.objects.all(),
        "especialidades": Especialidade.objects.all(),

    }
    return render(request, template_name, context)