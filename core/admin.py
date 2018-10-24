from django.contrib import admin
from .models import Especialidade, Medico, Cliente, Consulta, Convenio, Turno, EscalaTempo, DiaAgenda


# Register your models here.
@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao',)
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


@admin.register(Turno)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'inicio', 'fim',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'inicio', 'fim', )
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


@admin.register(EscalaTempo)
class EscalaTempoAdmin(admin.ModelAdmin):
    list_display = ('inicio', 'fim', 'turno')
    fieldsets = (
        (None, {
            'fields': ('inicio', 'fim', 'turno')
        }),
    )


class TurnosInline(admin.TabularInline):
    model = Turno
    extra = 3


@admin.register(DiaAgenda)
class DiaAgendaAdmin(admin.ModelAdmin):
    list_display = ('data', 'medico')
    inlines = (TurnosInline,)
    fieldsets = (
        (None, {
            'fields': ('data', 'medico')
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'data_nascimento', 'cpf', 'telefone',)
    fieldsets = (
        (None, {
            'fields': ('nome', 'sexo', 'data_nascimento', 'cpf', 'telefone','convenio')
        }),
    )


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('data', 'inicio', 'cliente', 'medico')
    fieldsets = (
        (None, {
            'fields': ('cliente', 'medico', 'data', 'inicio')
        }),
    )
