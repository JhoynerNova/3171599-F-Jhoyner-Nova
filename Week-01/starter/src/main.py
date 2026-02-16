# ============================================
# PROYECTO: API DE SEGUIMIENTO DE PAQUETES
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero
# ============================================

from fastapi import FastAPI

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

# Diccionario de saludos por idioma
GREETINGS: dict[str, str] = {
    "es": "¡Bienvenido al sistema de paquetes, {name}!",
    "en": "Welcome to the package tracking system, {name}!",
    "fr": "Bienvenue au système de suivi des colis, {name}!",
    "de": "Hallo, {name}!",
    "it": "Ciao, {name}!",
    "pt": "Olá, {name}!",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())

# ============================================
# TODO 1: CREAR LA INSTANCIA DE FASTAPI
# ============================================

app = FastAPI(
    title="Package Tracking API",
    description="API para seguimiento de paquetes en logística y transporte",
    version="1.0.0"
)

# ============================================
# TODO 2: ENDPOINT RAÍZ
# ============================================

@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información general de la API de seguimiento de paquetes."""
    return {
        "name": "Package Tracking API",
        "version": "1.0.0",
        "domain": "logistics",
        "docs": "/docs",
        "languages": SUPPORTED_LANGUAGES
    }

# ============================================
# TODO 3: BIENVENIDA PERSONALIZADA
# ============================================

@app.get("/welcome/{name}")
async def welcome(name: str, language: str = "es") -> dict[str, str]:
    """Mensaje de bienvenida personalizado en el idioma especificado."""
    template = GREETINGS.get(language, GREETINGS["es"])
    return {
        "message": template.format(name=name),
        "language": language,
        "customer": name
    }

# ============================================
# TODO 4: INFORMACIÓN DE ENTIDAD
# ============================================

@app.get("/entity/{name}/info")
async def entity_info(name: str, title: str = "Cliente") -> dict[str, str]:
    """Información formal de la entidad (cliente, empresa, etc.)."""
    greeting = f"Estimado/a {title} {name}, su información ha sido registrada en el sistema de logística."
    return {
        "greeting": greeting,
        "title": title,
        "entity": name
    }

# ============================================
# TODO 5: SERVICIO SEGÚN HORARIO
# ============================================

def get_service_period(hour: int) -> tuple[str, str]:
    """Determina el mensaje y período según la hora."""
    if 5 <= hour < 12:
        return ("Servicio matutino disponible", "morning")
    elif 12 <= hour < 18:
        return ("Servicio vespertino en operación", "afternoon")
    else:
        return ("Servicio nocturno en funcionamiento", "night")

@app.get("/service/{name}/time-based")
async def service_time_based(name: str, hour: int) -> dict[str, str | int]:
    """Servicio adaptado según el horario del día."""
    if hour < 0 or hour > 23:
        return {"error": "La hora debe estar entre 0 y 23"}
    mensaje, periodo = get_service_period(hour)
    return {
        "service_message": f"{mensaje}, {name}.",
        "hour": hour,
        "period": periodo
    }

# ============================================
# TODO 6: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Verifica el estado de la API."""
    return {
        "status": "healthy",
        "service": "package-tracking-api",
        "domain": "logistics",
        "version": "1.0.0"
    }
