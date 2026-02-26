"""
Router de Rutas de Envío
========================

CRUD completo para rutas de envío (categorías del dominio logístico).
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import routes_db, get_next_route_id
from schemas import RouteCreate, RouteUpdate, RouteResponse

router = APIRouter(
    prefix="/routes",
    tags=["Rutas de Envío"],
    responses={404: {"description": "Ruta no encontrada"}}
)


# ============================================
# GET /routes - Listar todas las rutas
# ============================================

@router.get("/", response_model=list[RouteResponse])
async def list_routes():
    """
    Listar todas las rutas de envío disponibles.
    """
    return list(routes_db.values())


# ============================================
# GET /routes/{id} - Obtener una ruta
# ============================================

@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: int = Path(..., gt=0, description="ID de la ruta")
):
    """
    Obtener una ruta de envío por su ID.
    """
    if route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ruta con ID {route_id} no encontrada"
        )
    return routes_db[route_id]


# ============================================
# POST /routes - Crear ruta
# ============================================

@router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(route: RouteCreate):
    """
    Crear una nueva ruta de envío.
    """
    new_id = get_next_route_id()
    new_route = {
        "id": new_id,
        **route.model_dump(),
        "created_at": datetime.now()
    }
    routes_db[new_id] = new_route
    return new_route


# ============================================
# PUT /routes/{id} - Reemplazar ruta completa
# ============================================

@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(
    route_id: int = Path(..., gt=0),
    route: RouteCreate = ...
):
    """
    Actualizar completamente una ruta de envío.
    """
    if route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ruta con ID {route_id} no encontrada"
        )
    updated_route = {
        "id": route_id,
        **route.model_dump(),
        "created_at": routes_db[route_id]["created_at"]
    }
    routes_db[route_id] = updated_route
    return updated_route


# ============================================
# DELETE /routes/{id} - Eliminar ruta
# ============================================

@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    route_id: int = Path(..., gt=0)
):
    """
    Eliminar una ruta de envío.
    """
    if route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ruta con ID {route_id} no encontrada"
        )
    del routes_db[route_id]
    return None
