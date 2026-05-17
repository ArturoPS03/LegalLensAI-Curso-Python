import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contrato
import os

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://ai-engine:8000")


def dashboard(request):
    contratos = Contrato.objects.all().order_by('-fecha_subida')
    return render(request, 'contratos/dashboard.html', {'contratos': contratos})


def subir_contrato(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        tipo = request.POST.get('tipo', 'alquiler')

        # Enviar PDF a FastAPI
        respuesta = requests.post(
            f"{AI_ENGINE_URL}/analizar-pdf?tipo={tipo}",
            files={"archivo": (archivo.name, archivo.read(), "application/pdf")}
        )

        if respuesta.status_code == 200:
            datos = respuesta.json()
            analisis = datos['analisis']

            # Guardar en base de datos
            contrato = Contrato.objects.create(
                nombre_archivo=datos['nombre_archivo'],
                tipo=tipo,
                firmantes=analisis.get('firmantes', []),
                fecha_contrato=analisis.get('fecha', ''),
                duracion=analisis.get('duracion', ''),
                importe=analisis.get('importe', ''),
                banderas_rojas=analisis.get('banderas_rojas', []),
                riesgo_total=analisis.get('riesgo_total', 'BAJO'),
                resumen=analisis.get('resumen', ''),
            )
            return redirect('informe', pk=contrato.pk)

    return render(request, 'contratos/subir.html')


def informe(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    return render(request, 'contratos/informe.html', {'contrato': contrato})
