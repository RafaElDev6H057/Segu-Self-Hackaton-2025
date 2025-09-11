# schemas/ia.py

from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    """
    Esquema para recibir un prompt del frontend.
    """
    prompt: str = Field(..., min_length=1, description="El texto que se enviará al modelo de IA.")