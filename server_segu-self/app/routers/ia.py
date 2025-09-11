# routers/ia.py

from fastapi import APIRouter, HTTPException, status
import google.generativeai as genai

from schemas.ia import PromptRequest

router = APIRouter(
    prefix="/ia",
    tags=["Inteligencia Artificial"]
)

@router.post("/analizar")
def analizar_datos(request: PromptRequest):
    """
    Recibe un prompt y devuelve un resumen generado por el modelo Gemini.
    """
    try:
        prompt = request.prompt
        
        # The line that causes the warning
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') # type: ignore

        response = model.generate_content(prompt)
        ai_summary = response.text

        return {"summary": ai_summary}

    except Exception as e:
        print(f"Ocurrió un error al contactar la API de Gemini: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al procesar la solicitud con la IA."
        )