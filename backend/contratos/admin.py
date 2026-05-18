from django.contrib import admin
from .models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'usuario', 'tipo', 'riesgo_total', 'num_banderas', 'fecha_subida']
    list_filter = ['tipo', 'riesgo_total', 'fecha_subida']
    search_fields = ['nombre_archivo', 'usuario__username']
    readonly_fields = ['firmantes', 'banderas_rojas', 'fecha_subida']
