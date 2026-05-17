import fitz
from fastapi import FastAPI, UploadFile, File, HTTPException
from contratos import crear_contrato

app = FastAPI(title="LegalLens AI Engine")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-engine"}


@app.get("/hola")
def hola():
    return {"mensaje": "¡Hola desde FastAPI! Los contenedores se hablan 🎉"}


@app.post("/analizar-pdf")
async def analizar_pdf(
    archivo: UploadFile = File(...),
    tipo: str = "alquiler"
):
    if not archivo.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF")

    contenido = await archivo.read()
    doc = fitz.open(stream=contenido, filetype="pdf")
    texto_completo = ""
    for num_pagina, pagina in enumerate(doc, start=1):
        texto_completo += f"\n--- Página {num_pagina} ---\n"
        texto_completo += pagina.get_text()
    num_paginas = len(doc)
    doc.close()

    try:
        contrato = crear_contrato(tipo, texto_completo)
        resultado = contrato.ejecutar_auditoria()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis IA: {str(e)}")

    return {
        "nombre_archivo": archivo.filename,
        "tipo_contrato": tipo,
        "num_paginas": num_paginas,
        "analisis": resultado
    }