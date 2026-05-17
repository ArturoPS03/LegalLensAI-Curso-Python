# LegalLens AI

SaaS para auditoría automática de contratos mediante Inteligencia Artificial.

## Requisitos
- Docker
- Docker Compose

## Instalación

1. Clona el repositorio
2. Crea el archivo `.env` en la raíz del proyecto:
GROQ_API_KEY=tu-api-key-aqui

Obtén tu API key gratuita en: https://console.groq.com/keys

3. Levanta el proyecto:
docker compose up --build

4. Abre http://localhost en el navegador

## Arquitectura

- **nginx-proxy** — Proxy inverso (puerto 80)
- **backend-django** — Panel de gestión y dashboard
- **ai-engine** — Motor de IA con FastAPI + LLaMA 3.3
- **db-legal** — Base de datos PostgreSQL

## Uso

1. Accede a http://localhost
2. Haz clic en "Subir contrato"
3. Selecciona el tipo (Alquiler o NDA)
4. Sube el PDF
5. La IA analiza y muestra las cláusulas abusivas detectadas
