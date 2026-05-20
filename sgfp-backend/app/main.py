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
    recurrentes,
    transacciones,
    usuarios
)
from app.core.configuracion import configuracion
from app.db.base import Base
from app.db.sesion import motor
from app.api.endpoints import administracion

# Crea todas las tablas en la base de datos al arrancar
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
# Basado en: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://sgfp-sistema-de-gesti-n-de-finanzas.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
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
app.include_router(
    recurrentes.enrutador,
    prefix="/recurrentes",
    tags=["Recurrentes"]
)

app.include_router(
    administracion.enrutador,
    prefix="/admin",
    tags=["Administración"]
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

    