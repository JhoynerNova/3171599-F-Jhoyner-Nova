"""
Router de Paquetes
==================

CRUD con filtrado avanzado, paginación y ordenamiento
para el sistema de seguimiento de paquetes.
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime
from math import ceil

from database import packages_db, routes_db, get_next_package_id
from schemas import PackageCreate, PackageUpdate, PackageResponse, SortOrder
from dependencies import PaginationDep, PackageFiltersDep, SortingDep

router = APIRouter(
    prefix="/packages",
    tags=["Paquetes"],
    responses={404: {"description": "Paquete no encontrado"}}
)


# ============================================
# HELPER: Enriquecer paquete con datos de ruta
# ============================================

def enrich_package(pkg: dict) -> dict:
    """Añade el objeto route al dict del paquete."""
    result = dict(pkg)
    result["route"] = routes_db.get(pkg["route_id"])
    return result


# ============================================
# GET /packages - Listar con filtros avanzados
# ============================================

@router.get("/")
async def list_packages(
    pagination: PaginationDep,
    filters: PackageFiltersDep,
    sorting: SortingDep
):
    """
    Listar paquetes con filtrado avanzado, paginación y ordenamiento.

    **Filtros disponibles:**
    - `search` → busca en tracking_code, description y recipient_name
    - `route_id` → filtra por ruta de envío
    - `status` → estado del paquete (pending, in_transit, delivered, failed)
    - `courier` → empresa courier (ej: DHL, FedEx, Coordinadora)
    - `is_fragile` → paquetes frágiles o no
    - `min_weight_kg` / `max_weight_kg` → rango de peso
    - `destination` → ciudad de destino (búsqueda parcial)
    - `origin` → ciudad de origen (búsqueda parcial)
    """
    items = list(packages_db.values())

    # --- Filtro: búsqueda en texto ---
    if filters.search:
        term = filters.search.lower()
        items = [
            p for p in items
            if term in p["tracking_code"].lower()
            or term in (p.get("description") or "").lower()
            or term in p["recipient_name"].lower()
        ]

    # --- Filtro: ruta de envío ---
    if filters.route_id is not None:
        items = [p for p in items if p["route_id"] == filters.route_id]

    # --- Filtro: estado ---
    if filters.status is not None:
        items = [p for p in items if p["status"] == filters.status.value]

    # --- Filtro: courier ---
    if filters.courier:
        term = filters.courier.lower()
        items = [p for p in items if term in p["courier"].lower()]

    # --- Filtro: frágil ---
    if filters.is_fragile is not None:
        items = [p for p in items if p["is_fragile"] == filters.is_fragile]

    # --- Filtro: peso mínimo ---
    if filters.min_weight_kg is not None:
        items = [p for p in items if p["weight_kg"] >= filters.min_weight_kg]

    # --- Filtro: peso máximo ---
    if filters.max_weight_kg is not None:
        items = [p for p in items if p["weight_kg"] <= filters.max_weight_kg]

    # --- Filtro: destino ---
    if filters.destination:
        term = filters.destination.lower()
        items = [p for p in items if term in p["destination"].lower()]

    # --- Filtro: origen ---
    if filters.origin:
        term = filters.origin.lower()
        items = [p for p in items if term in p["origin"].lower()]

    # --- Ordenamiento ---
    reverse = sorting.order == SortOrder.desc
    items = sorted(items, key=lambda p: p.get(sorting.sort_by.value, ""), reverse=reverse)

    # --- Paginación ---
    total = len(items)
    pages = ceil(total / pagination.per_page) if total > 0 else 1
    paginated = items[pagination.offset: pagination.offset + pagination.per_page]

    return {
        "items": [enrich_package(p) for p in paginated],
        "total": total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pages,
        "has_next": pagination.page < pages,
        "has_prev": pagination.page > 1
    }


# ============================================
# GET /packages/search - Búsqueda full-text
# ============================================

@router.get("/search")
async def search_packages(q: str):
    """
    Búsqueda full-text en todos los campos de texto del paquete.
    """
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El término de búsqueda debe tener al menos 2 caracteres"
        )
    term = q.lower()
    results = [
        enrich_package(p) for p in packages_db.values()
        if term in p["tracking_code"].lower()
        or term in (p.get("description") or "").lower()
        or term in p["recipient_name"].lower()
        or term in p["origin"].lower()
        or term in p["destination"].lower()
        or term in p["courier"].lower()
    ]
    return {"query": q, "total": len(results), "items": results}


# ============================================
# GET /packages/stats - Estadísticas por ruta
# ============================================

@router.get("/stats")
async def package_stats():
    """
    Estadísticas de paquetes agrupadas por ruta de envío.
    Incluye conteo por estado, peso promedio y peso total.
    """
    stats = {}

    for pkg in packages_db.values():
        route_id = pkg["route_id"]
        route = routes_db.get(route_id)
        route_name = route["name"] if route else f"Ruta {route_id}"

        if route_id not in stats:
            stats[route_id] = {
                "route_id": route_id,
                "route_name": route_name,
                "total_packages": 0,
                "total_weight_kg": 0.0,
                "by_status": {
                    "pending": 0,
                    "in_transit": 0,
                    "delivered": 0,
                    "failed": 0
                }
            }

        stats[route_id]["total_packages"] += 1
        stats[route_id]["total_weight_kg"] += pkg["weight_kg"]
        stats[route_id]["by_status"][pkg["status"]] += 1

    # Calcular peso promedio
    for s in stats.values():
        if s["total_packages"] > 0:
            s["avg_weight_kg"] = round(s["total_weight_kg"] / s["total_packages"], 2)
        else:
            s["avg_weight_kg"] = 0.0
        s["total_weight_kg"] = round(s["total_weight_kg"], 2)

    return {
        "total_packages": len(packages_db),
        "routes_summary": list(stats.values())
    }


# ============================================
# GET /packages/{id} - Obtener un paquete
# ============================================

@router.get("/{package_id}")
async def get_package(
    package_id: int = Path(..., gt=0, description="ID del paquete")
):
    """
    Obtener un paquete por su ID, incluyendo datos de su ruta.
    """
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paquete con ID {package_id} no encontrado"
        )
    return enrich_package(packages_db[package_id])


# ============================================
# POST /packages - Crear paquete
# ============================================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_package(package: PackageCreate):
    """
    Registrar un nuevo paquete en el sistema.
    """
    if package.route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La ruta con ID {package.route_id} no existe"
        )

    # Verificar peso contra límite de la ruta
    route = routes_db[package.route_id]
    if package.weight_kg > route["max_weight_kg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El paquete pesa {package.weight_kg}kg pero la ruta '{route['name']}' "
                   f"solo permite hasta {route['max_weight_kg']}kg"
        )

    new_id = get_next_package_id()
    new_package = {
        "id": new_id,
        **package.model_dump(),
        "status": package.status.value,
        "created_at": datetime.now()
    }
    packages_db[new_id] = new_package
    return enrich_package(new_package)


# ============================================
# PUT /packages/{id} - Reemplazar paquete
# ============================================

@router.put("/{package_id}")
async def replace_package(
    package_id: int = Path(..., gt=0),
    package: PackageCreate = ...
):
    """
    Reemplazar completamente los datos de un paquete.
    """
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paquete con ID {package_id} no encontrado"
        )
    if package.route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La ruta con ID {package.route_id} no existe"
        )

    updated = {
        "id": package_id,
        **package.model_dump(),
        "status": package.status.value,
        "created_at": packages_db[package_id]["created_at"]
    }
    packages_db[package_id] = updated
    return enrich_package(updated)


# ============================================
# PATCH /packages/{id} - Actualizar parcialmente
# ============================================

@router.patch("/{package_id}")
async def update_package(
    package_id: int = Path(..., gt=0),
    package: PackageUpdate = ...
):
    """
    Actualizar parcialmente un paquete (ej: cambiar estado o courier).
    """
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paquete con ID {package_id} no encontrado"
        )

    update_data = package.model_dump(exclude_unset=True)

    if "route_id" in update_data and update_data["route_id"] not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La ruta con ID {update_data['route_id']} no existe"
        )

    # Convertir enum a string si viene status
    if "status" in update_data and hasattr(update_data["status"], "value"):
        update_data["status"] = update_data["status"].value

    packages_db[package_id].update(update_data)
    return enrich_package(packages_db[package_id])


# ============================================
# DELETE /packages/{id} - Eliminar paquete
# ============================================

@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_package(
    package_id: int = Path(..., gt=0)
):
    """
    Eliminar un paquete del sistema.
    """
    if package_id not in packages_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paquete con ID {package_id} no encontrado"
        )
    del packages_db[package_id]
    return None


# ============================================
# GET /routes/{id}/packages - Paquetes de una ruta
# (endpoint extra requerido por el proyecto)
# ============================================

@router.get("/by-route/{route_id}")
async def packages_by_route(
    route_id: int = Path(..., gt=0, description="ID de la ruta de envío")
):
    """
    Listar todos los paquetes que pertenecen a una ruta de envío específica.
    """
    if route_id not in routes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ruta con ID {route_id} no encontrada"
        )
    pkgs = [enrich_package(p) for p in packages_db.values() if p["route_id"] == route_id]
    return {
        "route": routes_db[route_id],
        "total": len(pkgs),
        "packages": pkgs
    }
