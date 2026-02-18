# API de Gestión de Paquetes

Proyecto Semana 02 - Bootcamp

## Descripción
Este proyecto es una API REST para gestionar paquetes en un sistema de logística y transporte.  
Se construyó con **FastAPI** y **Pydantic v2**, y se ejecuta en **Docker**.

## Tecnologías
- Python 3.14
- FastAPI
- Pydantic
- Docker / Docker Compose
- Uvicorn

## Cómo ejecutar
1. Clonar el repositorio.
2. Construir y levantar el contenedor:
   ```bash
   docker compose up --build

- Abrir la documentación en el navegador:
http://localhost:8000/docs


Endpoints principales
- POST /packages → Crear paquete
- GET /packages → Listar paquetes
- GET /packages/{id} → Obtener paquete por ID
- GET /packages/tracking/{tracking_code} → Buscar por código de rastreo
- PATCH /packages/{id} → Actualizar paquete
- DELETE /packages/{id} → Eliminar paquete
Ejemplo de paquete
{
  "tracking_code": "AB12345678",
  "sender": "Carlos Pérez",
  "recipient": "María Gómez",
  "origin": "Bogotá",
  "destination": "Medellín",
  "weight": 2.5,
  "status": "pending",
  "is_fragile": true
}