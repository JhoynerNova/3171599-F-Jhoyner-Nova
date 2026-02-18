"""
Proyecto Semana 02: API de Gestión de Paquetes
===============================================

Aplicación FastAPI principal.
Los endpoints ya están definidos, debes completar schemas.py

Ejecutar:
    docker compose up --build
    
Documentación: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, status, Query
from datetime import datetime

# Importar los schemas que crearás
from schemas import (
    PackageCreate,
    PackageUpdate,
    PackageResponse,
    PackageList,
)
from database import packages_db, get_next_id, find_by_tracking_code

app = FastAPI(
    title="API de Gestión de Paquetes",
    description="Proyecto Semana 02 - Pydantic v2",
    version="1.0.0",
)


# ============================================
# ENDPOINTS
# ============================================

@app.post(
    "/packages",
    response_model=PackageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Packages"],
)
async def create_package(package: PackageCreate) -> PackageResponse:
    """
    Crear un nuevo paquete.
    
    - Valida que el tracking_code no exista
    """
    if find_by_tracking_code(package.tracking_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Package with tracking code {package.tracking_code} already exists"
        )
    
    package_id = get_next_id()
    new_package = {
        "id": package_id,
        **package.model_dump(),
        "created_at": datetime.now(),
        "updated_at": None,
    }
    packages_db[package_id] = new_package
    
    return new_package


@app.get(
    "/packages",
    response_model=PackageList,
    tags=["Packages"],
)
async def list_packages(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=100, default=10),
    status: str | None = None,
) -> PackageList:
    """
    Listar paquetes con paginación.
    
    - Soporta filtro por estado
    """
    packages = list(packages_db.values())
    if status:
        packages = [p for p in packages if p["status"] == status]
    
    total = len(packages)
    start = (page - 1) * per_page
    end = start + per_page
    items = packages[start:end]
    
    return PackageList(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@app.get(
    "/packages/{package_id}",
    response_model=PackageResponse,
    tags=["Packages"],
)
async def get_package(package_id: int) -> PackageResponse:
    """Obtener paquete por ID."""
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    return packages_db[package_id]


@app.get(
    "/packages/tracking/{tracking_code}",
    response_model=PackageResponse,
    tags=["Packages"],
)
async def get_package_by_tracking(tracking_code: str) -> PackageResponse:
    """Buscar paquete por código de rastreo."""
    package = find_by_tracking_code(tracking_code)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    return package


@app.patch(
    "/packages/{package_id}",
    response_model=PackageResponse,
    tags=["Packages"],
)
async def update_package(
    package_id: int,
    package: PackageUpdate,
) -> PackageResponse:
    """Actualizar paquete parcialmente."""
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    update_data = package.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    if "tracking_code" in update_data:
        existing = find_by_tracking_code(update_data["tracking_code"])
        if existing and existing["id"] != package_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tracking code {update_data['tracking_code']} already in use"
            )
    
    stored = packages_db[package_id]
    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()
    
    return stored


@app.delete(
    "/packages/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Packages"],
)
async def delete_package(package_id: int) -> None:
    """Eliminar paquete."""
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    del packages_db[package_id]


# ============================================
# HEALTH CHECK
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Health check."""
    return {
        "status": "ok",
        "message": "Packages API running",
        "total_packages": len(packages_db),
    }