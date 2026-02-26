"""
API de Seguimiento de Paquetes - Main
======================================

Punto de entrada de la aplicación.
Sistema de tracking para logística y transporte.
"""

from fastapi import FastAPI
from routers import categories, products

app = FastAPI(
    title="API de Seguimiento de Paquetes",
    description=(
        "API para gestión y seguimiento de paquetes en una empresa de logística. "
        "Permite registrar rutas de envío, crear paquetes, filtrarlos por múltiples "
        "criterios y consultar estadísticas por ruta."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(categories.router)   # /routes
app.include_router(products.router)     # /packages


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Seguimiento de Paquetes 📦",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "rutas": "/routes",
            "paquetes": "/packages",
            "busqueda": "/packages/search?q=término",
            "estadísticas": "/packages/stats"
        }
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}
