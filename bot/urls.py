"""bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index
from core.views import list_especialidades, webhook, list_consultas, list_convenio, cliente_detail, list_cliente, especialidade_data, list_medico, medico_detail, escalas_medico, especialidade_detail, medicos_especialidade

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls',
                                   'jet-dashboard')),  # Django JET dashboard URLS
    # path('admin/', include(admin.site.urls)),
    path('', index),
    path('especialidades/', list_especialidades.as_view(),
         name=list_especialidades.name),
    path('especialidade/<int:pk>/', especialidade_detail.as_view(),
         name=especialidade_detail.name),
    path('especialidade/<int:pk>/datas/', especialidade_data.as_view(), ),
    path('especialidade/<int:pk>/medicos',
         medicos_especialidade.as_view(), name=medicos_especialidade.name),
    path('medicos/', list_medico.as_view(), name=list_medico.name),
    path('medico/<int:pk>/', medico_detail.as_view(), name=medico_detail.name),
    path('medico/<int:pk>/agenda/', escalas_medico.as_view(), ),
    path('clientes/', list_cliente.as_view(), name=list_cliente.name),
    path('cliente/<int:pk>/', cliente_detail.as_view(), name=cliente_detail.name),
    path('convenios/', list_convenio.as_view(), name=list_convenio.name),
    path('consultas/', list_consultas.as_view(), name=list_consultas.name),
    path('webhook/', webhook),




]
