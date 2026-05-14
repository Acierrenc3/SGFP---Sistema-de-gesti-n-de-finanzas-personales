# Punto de entrada principal de la aplicación FastAPI
# Basado en: https://fastapi.tiangolo.com/tutorial/bigger-applications/

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    autenticacion,
    categorias,
    cuentas,
    dashboard,
    exportar,
    presupuestos,
    transacciones
)
from app.core.configuracion import configuracion
from app.db.base import Base
from app.db.sesion import motor
from app.api.endpoints import usuarios

# Crea todas las tablas en la base de datos al arrancar
# En producción se usará Alembic para las migraciones
Base.metadata.create_all(bind=motor)

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="SGFP - Sistema de Gestión de Finanzas Personales",
    description="API REST para la gestión de finanzas personales",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
# Permite peticiones desde el frontend (Vue) durante el desarrollo
# Basado en: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers con sus prefijos y etiquetas
# Basado en: https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-the-routers
app.include_router(
    autenticacion.enrutador,
    prefix="/auth",
    tags=["Autenticación"]
)
app.include_router(
    transacciones.enrutador,
    prefix="/transacciones",
    tags=["Transacciones"]
)
app.include_router(
    categorias.enrutador,
    prefix="/categorias",
    tags=["Categorías"]
)
app.include_router(
    presupuestos.enrutador,
    prefix="/presupuestos",
    tags=["Presupuestos"]
)
app.include_router(
    cuentas.enrutador,
    prefix="/cuentas",
    tags=["Cuentas"]
)
app.include_router(
    dashboard.enrutador,
    prefix="/dashboard",
    tags=["Dashboard"]
)
app.include_router(
    exportar.enrutador,
    prefix="/exportar",
    tags=["Exportar"]
)
app.include_router(
    usuarios.enrutador,
    prefix="/usuarios",
    tags=["Usuarios"]
)


@app.get("/", tags=["Estado"])
def estado():
    """Endpoint raíz para verificar que la API está en funcionamiento."""
    return {
        "estado": "activo",
        "aplicacion": "SGFP - Sistema de Gestión de Finanzas Personales",
        "version": "1.0.0",
        "documentacion": "/docs"
    }