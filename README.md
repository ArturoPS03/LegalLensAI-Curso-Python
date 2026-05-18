# LegalLens AI

Este proyecto consiste en una aplicación web que analizará contratos en PDF usando IA para detectar cláusulas abusivas o ilegales.

## Requisitos:
- Docker y Docker Compose instalados.

## Cómo ejecutarlo:

Primero hace falta una API key gratuita de Groq (el servicio de IA que usa el proyecto). Te la dan gratis registrándote en https://console.groq.com/keys.

Una vez la tengas, crea un archivo `.env` en la raíz del proyecto donde pegar la key:
GROQ_API_KEY=(KEY)

Luego levantar todo con:
docker compose up --build

Y abrir en: http://localhost.

## Estructura del proyecto:

El proyecto usa 4 contenedores Docker:

- **nginx** — hace de proxy, es el único que tiene el puerto 80 abierto.
- **backend-django** — la web, el dashboard y la base de datos.
- **ai-engine** — el microservicio FastAPI que lee los PDFs y llama a la IA.
- **db-legal** — PostgreSQL.

## POO - Cómo está organizado el código de análisis:

Hay una clase base `Contrato` con un método abstracto obtener_prompt_especifico(). Cada tipo de contrato hereda de ella y define qué tiene que buscar la IA:

- ContratoAlquiler — busca cualquier cosa ilegal.
- ContratoNDA — busca cláusulas abusivas típicas de los NDAs.

También hay una función crear_contrato() que recibe el tipo como string y devuelve el objeto correcto.

## Dataset de prueba:

En la carpeta `dataset/` hay 4 contratos PDF para probar:
- alquiler_contrato_legal.pdf — contrato de alquiler correcto.
- alquiler_contrato_trampa.pdf — contrato con cláusulas ilegales.
- nda_contrato_legal.pdf — NDA correcto.
- nda_contrato_trampa.pdf — NDA con cláusulas abusivas.