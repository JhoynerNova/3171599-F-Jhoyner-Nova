"""
Simulación de Base de Datos en memoria para Paquetes
"""

# "Base de datos" en memoria
packages_db: dict[int, dict] = {}

# Contador para IDs
_id_counter = 0


def get_next_id() -> int:
    """Obtener siguiente ID disponible."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def find_by_tracking_code(tracking_code: str) -> dict | None:
    """Buscar paquete por código de rastreo."""
    code_upper = tracking_code.upper()
    for package in packages_db.values():
        if package["tracking_code"].upper() == code_upper:
            return package
    return None


def reset_db() -> None:
    """Resetear base de datos (útil para tests)."""
    global _id_counter
    packages_db.clear()
    _id_counter = 0
