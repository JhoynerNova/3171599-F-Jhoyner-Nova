#  Package Tracking API (Bootcamp FastAPI Zero to Hero)

Este proyecto es parte de la **Semana 01 del Bootcamp FastAPI Zero to Hero**.  
La idea es construir una API sencilla para **seguimiento de paquetes en logística y transporte**, practicando conceptos básicos de FastAPI.

---

## Objetivos del proyecto

- Aprender a crear una API con **FastAPI**.
- Usar **type hints** para mayor claridad en el código.
- Practicar **path parameters** y **query parameters**.
- Explorar la documentación automática que genera FastAPI en `/docs`.
- Trabajar con **Docker** y levantar la API en un contenedor.

---

## Estructura del proyecto

starter/
├── src/
│   └── main.py        # Código principal de la API
├── Dockerfile         # Imagen de la aplicación
├── docker-compose.yml # Orquestación con Docker Compose
├── pyproject.toml     # Configuración de dependencias
├── uv.lock            # Archivo de bloqueo de dependencias
└── .dockerignore      # Archivos ignorados en la build


 Cómo correr la API

1. Construir y levantar el contenedor:
   ```bash
   docker compose up --build
Abrir en el navegador:

Documentación: http://localhost:8000/docs

Health check: http://localhost:8000/health

Endpoints implementados
1. Información general
GET /

json
{
  "name": "Package Tracking API",
  "version": "1.0.0",
  "domain": "logistics",
  "docs": "/docs",
  "languages": ["es", "en", "fr", "de", "it", "pt"]
}
2. Bienvenida personalizada
GET /welcome/{name}?language=en

json
{
  "message": "Welcome to the package tracking system, Jhoyner!",
  "language": "en",
  "customer": "Jhoyner"
}
3. Información de entidad
GET /entity/García/info?title=Dr.

json
{
  "greeting": "Estimado/a Dr. García, su información ha sido registrada en el sistema de logística.",
  "title": "Dr.",
  "entity": "García"
}
4. Servicio según horario
GET /service/Ana/time-based?hour=10

json
{
  "service_message": "Servicio matutino disponible, Ana.",
  "hour": 10,
  "period": "morning"
}
5. Health check
GET /health

json
{
  "status": "healthy",
  "service": "package-tracking-api",
  "domain": "logistics",
  "version": "1.0.0"
}
Tecnologías usadas
Python 3.11

FastAPI

Uvicorn

Docker / Docker Compose