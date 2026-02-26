"""
Dependencias Reutilizables
==========================

Define dependencias para paginación, filtros y ordenamiento
adaptadas al dominio de seguimiento de paquetes.
"""

from fastapi import Query, Depends
from typing import Annotated
from schemas import SortOrder, PackageSortField, PackageStatus


# ============================================
# PAGINACIÓN
# ============================================

class PaginationParams:
    """
    Dependencia para parámetros de paginación.
    - page: número de página (default 1)
    - per_page: ítems por página (default 10, máx 50)
    - offset: calculado automáticamente
    """

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Número de página"),
        per_page: int = Query(default=10, ge=1, le=50, description="Paquetes por página")
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page


PaginationDep = Annotated[PaginationParams, Depends()]


# ============================================
# FILTROS DE PAQUETES
# ============================================

class PackageFilters:
    """
    Dependencia para filtros de búsqueda de paquetes.

    Filtros disponibles (mínimo 6):
    - search         → busca en tracking_code, description y recipient_name
    - route_id       → filtra por ruta de envío
    - status         → filtra por estado del paquete (pending, in_transit, delivered, failed)
    - courier        → filtra por empresa courier
    - is_fragile     → solo paquetes frágiles o no frágiles
    - min_weight_kg  → peso mínimo en kg
    - max_weight_kg  → peso máximo en kg
    - destination    → filtra por ciudad de destino (búsqueda parcial)
    - origin         → filtra por ciudad de origen (búsqueda parcial)
    """

    def __init__(
        self,
        search: str | None = Query(
            default=None,
            min_length=2,
            description="Busca en código de rastreo, descripción o destinatario"
        ),
        route_id: int | None = Query(
            default=None,
            gt=0,
            description="Filtrar por ID de ruta de envío"
        ),
        status: PackageStatus | None = Query(
            default=None,
            description="Filtrar por estado: pending, in_transit, delivered, failed"
        ),
        courier: str | None = Query(
            default=None,
            min_length=2,
            description="Filtrar por empresa courier (ej: DHL, FedEx)"
        ),
        is_fragile: bool | None = Query(
            default=None,
            description="Filtrar paquetes frágiles (true) o no frágiles (false)"
        ),
        min_weight_kg: float | None = Query(
            default=None,
            ge=0,
            description="Peso mínimo del paquete en kg"
        ),
        max_weight_kg: float | None = Query(
            default=None,
            ge=0,
            description="Peso máximo del paquete en kg"
        ),
        destination: str | None = Query(
            default=None,
            min_length=2,
            description="Filtrar por ciudad de destino (búsqueda parcial)"
        ),
        origin: str | None = Query(
            default=None,
            min_length=2,
            description="Filtrar por ciudad de origen (búsqueda parcial)"
        ),
    ):
        self.search = search
        self.route_id = route_id
        self.status = status
        self.courier = courier
        self.is_fragile = is_fragile
        self.min_weight_kg = min_weight_kg
        self.max_weight_kg = max_weight_kg
        self.destination = destination
        self.origin = origin


PackageFiltersDep = Annotated[PackageFilters, Depends()]


# ============================================
# ORDENAMIENTO
# ============================================

class SortingParams:
    """
    Dependencia para ordenamiento de paquetes.
    - sort_by: campo por el que ordenar (default: created_at)
    - order: asc o desc (default: desc)
    """

    def __init__(
        self,
        sort_by: PackageSortField = Query(
            default=PackageSortField.created_at,
            description="Campo por el que ordenar"
        ),
        order: SortOrder = Query(
            default=SortOrder.desc,
            description="Orden: asc (ascendente) o desc (descendente)"
        )
    ):
        self.sort_by = sort_by
        self.order = order


SortingDep = Annotated[SortingParams, Depends()]
