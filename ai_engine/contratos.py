from abc import ABC, abstractmethod
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class Contrato(ABC):
    def __init__(self, texto: str):
        self.texto = texto

    @abstractmethod
    def obtener_prompt_especifico(self) -> str:
        pass

    def ejecutar_auditoria(self) -> dict:
        prompt = f"""{self.obtener_prompt_especifico()}

Analiza el siguiente contrato y responde SOLO con este JSON sin texto adicional ni marcadores de código:
{{
  "firmantes": ["nombre1", "nombre2"],
  "fecha": "fecha del contrato",
  "duracion": "duración del contrato",
  "importe": "importe o fianza si aplica",
  "banderas_rojas": [
    {{
      "clausula": "texto literal de la cláusula problemática",
      "problema": "explicación del problema legal",
      "gravedad": "ALTA/MEDIA/BAJA"
    }}
  ],
  "riesgo_total": "CRITICO/MEDIO/BAJO",
  "resumen": "resumen breve del análisis"
}}

TEXTO DEL CONTRATO:
{self.texto[:6000]}"""

        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        texto_respuesta = respuesta.choices[0].message.content.strip()
        texto_respuesta = texto_respuesta.replace("```json", "").replace("```", "").strip()
        return json.loads(texto_respuesta)


class ContratoAlquiler(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """Eres un abogado experto en derecho español. Analiza este contrato de alquiler buscando:
- Fianza ilegal (debe ser máximo 1 mes para vivienda habitual)
- Reparaciones estructurales cargadas al inquilino (ilegal según Art. 21 LAU)
- Acceso del casero sin preaviso (ilegal)
- Cláusulas de desahucio express privado (ilegal)
- Gastos de inmobiliaria al inquilino (ilegal desde 2023)
- Cualquier cláusula que contradiga la LAU"""


class ContratoNDA(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """Eres un abogado experto en derecho español. Analiza este contrato de confidencialidad (NDA) buscando:
- Duración infinita o perpetua (abusiva)
- Multas desproporcionadas (más de 100.000€ para trabajadores individuales)
- Objeto difuso (todo lo que piense o diga el trabajador)
- Unilateralidad absoluta (solo el trabajador tiene obligaciones)
- Jurisdicción en países exóticos fuera de España
- Cualquier cláusula abusiva según el derecho laboral español"""


def crear_contrato(tipo: str, texto: str) -> Contrato:
    if tipo == "alquiler":
        return ContratoAlquiler(texto)
    elif tipo == "nda":
        return ContratoNDA(texto)
    else:
        raise ValueError(f"Tipo de contrato desconocido: {tipo}")
