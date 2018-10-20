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
from django.urls import path
from core.views import index
from core.views import list_especialidades, list_medico, medico_detail, escalas_medico

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('especialidades/', list_especialidades.as_view(),name=list_especialidades.name),
    path('medicos/', list_medico.as_view(),name=list_medico.name),
    path('medico/<int:pk>/', medico_detail.as_view(), name=medico_detail.name),
    path('medico/<int:pk>/agenda/', escalas_medico.as_view(), ),


]
