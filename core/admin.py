from django.contrib import admin
from .models import Especialidade, Medico


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
    list_display = ('nome','crm','especialidade')
    fieldsets = (
        (None, {
            'fields': ('nome','crm','especialidade')
        }),
    )