from django.db import models


class Contrato(models.Model):
    TIPO_CHOICES = [
        ('alquiler', 'Contrato de Alquiler'),
        ('nda', 'Acuerdo de Confidencialidad'),
    ]
    RIESGO_CHOICES = [
        ('CRITICO', 'Crítico'),
        ('MEDIO', 'Medio'),
        ('BAJO', 'Bajo'),
    ]

    nombre_archivo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    firmantes = models.JSONField(default=list)
    fecha_contrato = models.CharField(max_length=100, blank=True)
    duracion = models.CharField(max_length=200, blank=True)
    importe = models.CharField(max_length=200, blank=True)
    banderas_rojas = models.JSONField(default=list)
    riesgo_total = models.CharField(max_length=20, choices=RIESGO_CHOICES, blank=True)
    resumen = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre_archivo} - {self.riesgo_total}"

    def num_banderas(self):
        return len(self.banderas_rojas)
