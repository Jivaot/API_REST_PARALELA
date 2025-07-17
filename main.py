# main.py

from fastapi import FastAPI
from database import db
from routers.genders import router as genders_router
from routers.species import router as species_router
from routers.strata import router as strata_router
from routers.stats import router as stats_router

app = FastAPI(
    title="Un API de otro mundo",
    description=(
        "Documentación de la API del trabajo Isekai (simulado) como parte "
        "de la asignatura Computación Paralela y Distribuida de la UTEM "
        "semestre de otoño 2025."
    ),
    version="1.0.0",
)

@app.on_event("startup")
async def on_startup():
    """Inicializa el pool al arrancar la aplicación."""
    await db.connect()

@app.on_event("shutdown")
async def on_shutdown():
    """Cierra el pool al detener la aplicación."""
    await db.disconnect()

# Monta tus routers SIN volver a poner prefix/tags aquí
app.include_router(genders_router)
app.include_router(species_router)
app.include_router(strata_router)
app.include_router(stats_router)

@app.get("/", summary="Ruta raíz", tags=["Información base"])
async def root():
    return {"message": "Bienvenido a la API Isekai de otro mundo"}
