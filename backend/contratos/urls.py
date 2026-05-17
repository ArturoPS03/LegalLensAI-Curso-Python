from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('subir/', views.subir_contrato, name='subir_contrato'),
    path('informe/<int:pk>/', views.informe, name='informe'),
]
