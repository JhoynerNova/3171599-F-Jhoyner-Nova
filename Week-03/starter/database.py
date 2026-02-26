"""
Base de Datos Simulada
======================

Datos en memoria para el sistema de seguimiento de paquetes.
"""

from datetime import datetime

# ============================================
# RUTAS DE ENVÍO (Categories)
# ============================================

routes_db: dict[int, dict] = {
    1: {
        "id": 1,
        "code": "NAC-EXP",
        "name": "Nacional Express",
        "description": "Envíos nacionales con entrega en 24-48 horas",
        "max_weight_kg": 30.0,
        "is_international": False,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    2: {
        "id": 2,
        "code": "NAC-STD",
        "name": "Nacional Estándar",
        "description": "Envíos nacionales con entrega en 3-5 días hábiles",
        "max_weight_kg": 50.0,
        "is_international": False,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "code": "INT-EXP",
        "name": "Internacional Express",
        "description": "Envíos internacionales con entrega en 2-4 días hábiles",
        "max_weight_kg": 20.0,
        "is_international": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
    4: {
        "id": 4,
        "code": "INT-ECO",
        "name": "Internacional Económico",
        "description": "Envíos internacionales con entrega en 10-20 días hábiles",
        "max_weight_kg": 25.0,
        "is_international": True,
        "created_at": datetime(2024, 1, 1, 10, 0, 0)
    },
}

next_route_id = 5

# ============================================
# PAQUETES (Main Entity)
# ============================================

packages_db: dict[int, dict] = {
    1: {
        "id": 1,
        "tracking_code": "PKG-2024-001",
        "description": "Laptop y accesorios electrónicos",
        "route_id": 1,
        "status": "delivered",
        "weight_kg": 2.5,
        "origin": "Bogotá",
        "destination": "Medellín",
        "courier": "ServientregA",
        "recipient_name": "Carlos Pérez",
        "is_fragile": True,
        "created_at": datetime(2024, 1, 15, 9, 0, 0)
    },
    2: {
        "id": 2,
        "tracking_code": "PKG-2024-002",
        "description": "Ropa y calzado deportivo",
        "route_id": 2,
        "status": "in_transit",
        "weight_kg": 1.2,
        "origin": "Cali",
        "destination": "Barranquilla",
        "courier": "Coordinadora",
        "recipient_name": "Ana Gómez",
        "is_fragile": False,
        "created_at": datetime(2024, 2, 1, 10, 0, 0)
    },
    3: {
        "id": 3,
        "tracking_code": "PKG-2024-003",
        "description": "Documentos legales certificados",
        "route_id": 3,
        "status": "in_transit",
        "weight_kg": 0.3,
        "origin": "Bogotá",
        "destination": "Miami",
        "courier": "DHL",
        "recipient_name": "Luis Martínez",
        "is_fragile": False,
        "created_at": datetime(2024, 1, 20, 14, 0, 0)
    },
    4: {
        "id": 4,
        "tracking_code": "PKG-2024-004",
        "description": "Repuestos industriales",
        "route_id": 4,
        "status": "pending",
        "weight_kg": 15.0,
        "origin": "Medellín",
        "destination": "Ciudad de México",
        "courier": "FedEx",
        "recipient_name": "Empresa MexTech",
        "is_fragile": False,
        "created_at": datetime(2024, 3, 1, 8, 0, 0)
    },
    5: {
        "id": 5,
        "tracking_code": "PKG-2024-005",
        "description": "Artículos de vidrio y cerámica",
        "route_id": 1,
        "status": "pending",
        "weight_kg": 3.8,
        "origin": "Bucaramanga",
        "destination": "Bogotá",
        "courier": "ServientregA",
        "recipient_name": "María Torres",
        "is_fragile": True,
        "created_at": datetime(2024, 2, 15, 11, 0, 0)
    },
    6: {
        "id": 6,
        "tracking_code": "PKG-2024-006",
        "description": "Libros universitarios",
        "route_id": 2,
        "status": "delivered",
        "weight_kg": 4.5,
        "origin": "Bogotá",
        "destination": "Pereira",
        "courier": "Coordinadora",
        "recipient_name": "Juan Rodríguez",
        "is_fragile": False,
        "created_at": datetime(2024, 2, 20, 16, 0, 0)
    },
    7: {
        "id": 7,
        "tracking_code": "PKG-2024-007",
        "description": "Equipo fotográfico profesional",
        "route_id": 3,
        "status": "failed",
        "weight_kg": 5.0,
        "origin": "Bogotá",
        "destination": "Buenos Aires",
        "courier": "DHL",
        "recipient_name": "Studio ARG",
        "is_fragile": True,
        "created_at": datetime(2024, 3, 5, 9, 0, 0)
    },
    8: {
        "id": 8,
        "tracking_code": "PKG-2024-008",
        "description": "Muestras de café especial",
        "route_id": 4,
        "status": "in_transit",
        "weight_kg": 8.0,
        "origin": "Armenia",
        "destination": "Madrid",
        "courier": "FedEx",
        "recipient_name": "Café Europa SL",
        "is_fragile": False,
        "created_at": datetime(2024, 3, 10, 10, 0, 0)
    },
}

next_package_id = 9


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_next_route_id() -> int:
    """Obtener y incrementar ID de ruta"""
    global next_route_id
    current = next_route_id
    next_route_id += 1
    return current


def get_next_package_id() -> int:
    """Obtener y incrementar ID de paquete"""
    global next_package_id
    current = next_package_id
    next_package_id += 1
    return current
