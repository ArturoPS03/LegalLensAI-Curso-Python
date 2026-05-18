import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Contrato
import os

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://ai-engine:8000")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'contratos/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    contratos = Contrato.objects.filter(usuario=request.user).order_by('-fecha_subida')
    return render(request, 'contratos/dashboard.html', {'contratos': contratos})


@login_required
def subir_contrato(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        tipo = request.POST.get('tipo', 'alquiler')

        respuesta = requests.post(
            f"{AI_ENGINE_URL}/analizar-pdf?tipo={tipo}",
            files={"archivo": (archivo.name, archivo.read(), "application/pdf")}
        )

        if respuesta.status_code == 200:
            datos = respuesta.json()
            analisis = datos['analisis']

            contrato = Contrato.objects.create(
                usuario=request.user,
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


@login_required
def informe(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk, usuario=request.user)
    return render(request, 'contratos/informe.html', {'contrato': contrato})
