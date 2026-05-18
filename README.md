# LegalLens AI

Este proyecto consiste en una aplicación web que analiza contratos en PDF usando IA para detectar cláusulas abusivas o ilegales.

## Requisitos

- Docker y Docker Compose instalados.

## Cómo ejecutarlo:

Primero hace falta una API key gratuita de Groq (el servicio de IA que usa el proyecto). Te la dan gratis registrándote en https://console.groq.com/keys.

Al tener la API key hay que crear un archivo `.env` en la raíz del proyecto y pegarlo:
GROQ_API_KEY=key-aqui

Luego levantar todo con:
docker compose up --build

La primera vez tarda un poco en construir las imágenes. Cuando termine, crear un usuario para acceder a la aplicación:
docker compose exec backend-django python manage.py createsuperuser

Abrir http://localhost e iniciar sesión con el usuario recién creado.

## Estructura del proyecto:

El proyecto usa 4 contenedores Docker:

- **nginx** — hace de proxy, es el único que tiene el puerto 80 abierto.
- **backend-django** — la web, el dashboard y la base de datos.
- **ai-engine** — el microservicio FastAPI que lee los PDFs y llama a la IA.
- **db-legal** — PostgreSQL.

## POO - Cómo está organizado el código de análisis:

Hay una clase base `Contrato` con un método abstracto `obtener_prompt_especifico()`. Cada tipo de contrato hereda de ella y define qué tiene que buscar la IA:

- ContratoAlquiler — busca infracciones de la LAU (fianza, reparaciones estructurales, acceso sin preaviso, etc.).
- ContratoNDA — busca cláusulas abusivas típicas de los NDAs.

También hay una función `crear_contrato()` que recibe el tipo como string y devuelve el objeto correcto. Si en el futuro se quisiera añadir un nuevo tipo solo habría que crear una clase nueva sin tocar el resto.

## Dataset de prueba:

En la carpeta `dataset/` hay 4 contratos PDF para probar:

- alquiler_correcto.pdf — contrato de alquiler correcto.
- alquiler_incorrecto.pdf — contrato con cláusulas ilegales.
- confidencialidad_correcto.pdf — NDA correcto.
- confidencialidad_incorrecto.pdf — NDA con cláusulas abusivas.
