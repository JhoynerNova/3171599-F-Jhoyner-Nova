"""
Schemas Pydantic
================

Modelos de datos para el sistema de seguimiento de paquetes.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class SortOrder(str, Enum):
    """Orden de clasificación"""
    asc = "asc"
    desc = "desc"


class PackageSortField(str, Enum):
    """Campos para ordenar paquetes"""
    tracking_code = "tracking_code"
    weight_kg = "weight_kg"
    created_at = "created_at"
    status = "status"
    destination = "destination"


class PackageStatus(str, Enum):
    """Estados posibles de un paquete"""
    pending = "pending"         # Registrado, aún no recogido
    in_transit = "in_transit"   # En camino
    delivered = "delivered"     # Entregado exitosamente
    failed = "failed"           # Entrega fallida


# ============================================
# ROUTE SCHEMAS (Categorías = Rutas de envío)
# ============================================

class RouteBase(BaseModel):
    """Schema base para rutas de envío"""
    code: str = Field(..., min_length=2, max_length=20, description="Código único de la ruta (ej: NAC-EXP)")
    name: str = Field(..., min_length=2, max_length=100, description="Nombre descriptivo de la ruta")
    description: str | None = Field(default=None, max_length=300)
    max_weight_kg: float = Field(..., gt=0, description="Peso máximo permitido en kg")
    is_international: bool = Field(default=False, description="¿Es ruta internacional?")


class RouteCreate(RouteBase):
    """Schema para crear una ruta"""
    pass


class RouteUpdate(BaseModel):
    """Schema para actualizar una ruta (todos los campos opcionales)"""
    code: str | None = Field(default=None, min_length=2, max_length=20)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    max_weight_kg: float | None = Field(default=None, gt=0)
    is_international: bool | None = None


class RouteResponse(RouteBase):
    """Schema de respuesta para una ruta"""
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================
# PACKAGE SCHEMAS (Entidad principal = Paquetes)
# ============================================

class PackageBase(BaseModel):
    """Schema base para paquetes"""
    tracking_code: str = Field(..., min_length=3, max_length=50, description="Código de rastreo único (ej: PKG-2024-001)")
    description: str | None = Field(default=None, max_length=500, description="Descripción del contenido")
    weight_kg: float = Field(..., gt=0, description="Peso del paquete en kg")
    origin: str = Field(..., min_length=2, max_length=100, description="Ciudad de origen")
    destination: str = Field(..., min_length=2, max_length=100, description="Ciudad de destino")
    courier: str = Field(..., min_length=2, max_length=100, description="Empresa courier encargada")
    recipient_name: str = Field(..., min_length=2, max_length=150, description="Nombre del destinatario")
    is_fragile: bool = Field(default=False, description="¿Contiene artículos frágiles?")


class PackageCreate(PackageBase):
    """Schema para crear un paquete"""
    route_id: int = Field(..., gt=0, description="ID de la ruta de envío")
    status: PackageStatus = Field(default=PackageStatus.pending, description="Estado inicial del paquete")


class PackageUpdate(BaseModel):
    """Schema para actualización parcial de un paquete"""
    tracking_code: str | None = Field(default=None, min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    route_id: int | None = Field(default=None, gt=0)
    status: PackageStatus | None = None
    weight_kg: float | None = Field(default=None, gt=0)
    origin: str | None = Field(default=None, min_length=2, max_length=100)
    destination: str | None = Field(default=None, min_length=2, max_length=100)
    courier: str | None = Field(default=None, min_length=2, max_length=100)
    recipient_name: str | None = Field(default=None, min_length=2, max_length=150)
    is_fragile: bool | None = None


class PackageResponse(PackageBase):
    """Schema de respuesta para un paquete"""
    id: int
    route_id: int
    status: PackageStatus
    created_at: datetime
    route: RouteResponse | None = None

    model_config = {"from_attributes": True}


# ============================================
# PAGINATION SCHEMAS
# ============================================

class PaginatedResponse(BaseModel):
    """Schema para respuestas paginadas"""
    items: list
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool
