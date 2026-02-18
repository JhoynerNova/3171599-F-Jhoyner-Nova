"""
Schemas Pydantic para la API de Paquetes
=========================================

Schemas requeridos:
- PackageBase: Campos comunes
- PackageCreate: Para POST (con validadores)
- PackageUpdate: Para PATCH (todos opcionales)
- PackageResponse: Para respuestas
- PackageList: Lista paginada
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from decimal import Decimal
import re
from enum import Enum


# ============================================
# Enum de estados
# ============================================

class StatusEnum(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"
    returned = "returned"


# ============================================
# PackageBase
# ============================================

class PackageBase(BaseModel):
    tracking_code: str = Field(..., min_length=10, max_length=10)
    sender: str = Field(..., min_length=2, max_length=100)
    recipient: str = Field(..., min_length=2, max_length=100)
    origin: str = Field(..., min_length=2, max_length=100)
    destination: str = Field(..., min_length=2, max_length=100)
    weight: Decimal = Field(..., gt=0)
    status: StatusEnum = StatusEnum.pending
    is_fragile: bool = False


# ============================================
# PackageCreate
# ============================================

class PackageCreate(PackageBase):
    """Schema para crear un paquete."""

    @field_validator("tracking_code")
    def validate_tracking_code(cls, v: str) -> str:
        # Formato: 2 letras + 8 números (ej: AB12345678)
        if not re.match(r"^[A-Z]{2}\d{8}$", v):
            raise ValueError("Tracking code must be format: XX12345678")
        return v.upper()

    @field_validator("weight")
    def validate_weight(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Weight must be greater than 0")
        return round(v, 2)

    @field_validator("sender", "recipient", "origin", "destination")
    def normalize_strings(cls, v: str) -> str:
        return v.strip().title()


# ============================================
# PackageUpdate
# ============================================

class PackageUpdate(BaseModel):
    tracking_code: str | None = None
    sender: str | None = None
    recipient: str | None = None
    origin: str | None = None
    destination: str | None = None
    weight: Decimal | None = None
    status: StatusEnum | None = None
    is_fragile: bool | None = None

    @field_validator("tracking_code")
    def validate_tracking_code(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not re.match(r"^[A-Z]{2}\d{8}$", v):
            raise ValueError("Tracking code must be format: XX12345678")
        return v.upper()

    @field_validator("weight")
    def validate_weight(cls, v: Decimal | None) -> Decimal | None:
        if v is None:
            return v
        if v <= 0:
            raise ValueError("Weight must be greater than 0")
        return round(v, 2)

    @field_validator("sender", "recipient", "origin", "destination")
    def normalize_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().title()


# ============================================
# PackageResponse
# ============================================

class PackageResponse(PackageBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ============================================
# PackageList
# ============================================

class PackageList(BaseModel):
    items: list[PackageResponse]
    total: int
    page: int
    per_page: int