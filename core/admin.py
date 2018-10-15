from django.contrib import admin
from .models import Especialidade, Medico, Cliente, Consulta, Convenio


# Register your models here.
@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fieldsets = (
        (None, {
            'fields': ('nome',)
        }),
    )


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm', 'especialidade')
    fieldsets = (
        (None, {
            'fields': ('nome', 'crm', 'especialidade')
        }),
    )


@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fieldsets = (
        (None, {
            'fields': ('nome',)
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    fieldsets = (
        (None, {
            'fields': ('nome',)
        }),
    )


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('convenio', 'cliente', 'medico')
    fieldsets = (
        (None, {
            'fields': ('convenio', 'cliente', 'medico')
        }),
    )
