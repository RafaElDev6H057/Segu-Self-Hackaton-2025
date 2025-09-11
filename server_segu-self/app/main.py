# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORTACIONES MODIFICADAS ---
import google.generativeai as genai
from core.config import GOOGLE_API_KEY # Importa la variable directamente

# --- Importaciones existentes ---
from core.db import create_db_and_tables
from routers import user, advertencia, reporte, ia


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",   
]

# --- CONFIGURACIÓN DEL CLIENTE DE GEMINI ---
# Se configura una sola vez usando la variable importada.
try:
    # Añadimos el comentario para ignorar el falso positivo del linter
    genai.configure(api_key=GOOGLE_API_KEY) # type: ignore
    
    print("Cliente de Google Generative AI configurado exitosamente.")
except Exception as e:
    print(f"ERROR: No se pudo configurar el cliente de Google Generative AI: {e}")

# --- El resto del archivo sigue igual ---

app = FastAPI(
    title="Mi Proyecto de Backend",
    description="API para gestionar usuarios, advertencias, reportes e IA.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluimos TODOS los routers
app.include_router(user.router)
app.include_router(advertencia.router)
app.include_router(reporte.router)
app.include_router(ia.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "¡Bienvenido a la API!"}