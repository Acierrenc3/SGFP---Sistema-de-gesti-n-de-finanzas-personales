# Endpoints de autenticación: registro y login
# Basado en: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.seguridad import (
    crear_token_acceso,
    obtener_hash_contraseña,
    verificar_contraseña
)
from app.db.sesion import obtener_sesion
from app.esquemas.usuario import TokenAcceso, UsuarioCrear, UsuarioRespuesta
from app.modelos.usuario import Usuario

# Instancia del router para agrupar los endpoints de autenticación
enrutador = APIRouter()

# Esquema OAuth2 que indica la URL donde se obtiene el token
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/auth/token")


def obtener_usuario_actual(
    token: str = Depends(oauth2_esquema),
    sesion: Session = Depends(obtener_sesion)
) -> Usuario:
    """
    Dependencia que extrae y valida el usuario autenticado desde el token JWT.
    Se usa en los endpoints protegidos.
    """
    from app.core.seguridad import decodificar_token

    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodificar_token(token)
    if payload is None:
        raise credenciales_exception

    email: str = payload.get("sub")
    if email is None:
        raise credenciales_exception

    # Busca el usuario en la base de datos
    usuario = sesion.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credenciales_exception

    return usuario


@enrutador.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de nuevo usuario"
)
def registrar_usuario(
    datos: UsuarioCrear,
    sesion: Session = Depends(obtener_sesion)
):
    """
    Registra un nuevo usuario en el sistema.
    Verifica que el email no esté ya registrado antes de crear el usuario.
    """
    # Comprueba si el email ya existe
    usuario_existente = sesion.query(Usuario).filter(
        Usuario.email == datos.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Crea el nuevo usuario con la contraseña hasheada
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        contrasena_hash=obtener_hash_contraseña(datos.contrasena),
        moneda=datos.moneda,
        zona_horaria=datos.zona_horaria
    )

    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)

    return nuevo_usuario


@enrutador.post(
    "/token",
    response_model=TokenAcceso,
    summary="Login y obtención de token JWT"
)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    sesion: Session = Depends(obtener_sesion)
):
    """
    Autentica al usuario con email y contraseña.
    Devuelve un token JWT si las credenciales son correctas.
    OAuth2PasswordRequestForm espera los campos 'username' y 'password'.
    En este proyecto 'username' corresponde al email del usuario.
    """
    # Busca el usuario por email
    usuario = sesion.query(Usuario).filter(
        Usuario.email == formulario.username
    ).first()

    # Verifica que el usuario existe y la contraseña es correcta
    if not usuario or not verificar_contraseña(formulario.password, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica que la cuenta está activa
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario inactiva"
        )

    # Genera el token JWT con el email como subject
    token = crear_token_acceso(datos={"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}

    # Endpoints de autenticación: registro y login
# Basado en: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.seguridad import (
    crear_token_acceso,
    crear_refresh_token,
    obtener_hash_contraseña,
    verificar_contraseña
)
from app.esquemas.usuario import TokenAcceso, UsuarioCrear, UsuarioRespuesta, RefreshToken
from app.db.sesion import obtener_sesion
from app.modelos.categoria import Categoria
from app.modelos.usuario import Usuario

enrutador = APIRouter()
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Categorías predefinidas que se asignan a cada nuevo usuario
CATEGORIAS_PREDEFINIDAS = [
    # Gastos
    { "nombre": "Alimentación", "icono": "pi-shopping-cart", "color": "#F59E0B", "tipo": "gasto" },
    { "nombre": "Transporte", "icono": "pi-car", "color": "#3B82F6", "tipo": "gasto" },
    { "nombre": "Ocio", "icono": "pi-star", "color": "#8B5CF6", "tipo": "gasto" },
    { "nombre": "Salud", "icono": "pi-heart", "color": "#EF4444", "tipo": "gasto" },
    { "nombre": "Hogar", "icono": "pi-home", "color": "#10B981", "tipo": "gasto" },
    { "nombre": "Ropa", "icono": "pi-tag", "color": "#EC4899", "tipo": "gasto" },
    { "nombre": "Educación", "icono": "pi-book", "color": "#06B6D4", "tipo": "gasto" },
    { "nombre": "Restaurantes", "icono": "pi-globe", "color": "#F97316", "tipo": "gasto" },
    { "nombre": "Suscripciones", "icono": "pi-sync", "color": "#6366F1", "tipo": "gasto" },
    { "nombre": "Otros gastos", "icono": "pi-ellipsis-h", "color": "#6B7280", "tipo": "gasto" },
    # Ingresos
    { "nombre": "Salario", "icono": "pi-briefcase", "color": "#10B981", "tipo": "ingreso" },
    { "nombre": "Freelance", "icono": "pi-desktop", "color": "#3B82F6", "tipo": "ingreso" },
    { "nombre": "Inversiones", "icono": "pi-chart-line", "color": "#8B5CF6", "tipo": "ingreso" },
    { "nombre": "Otros ingresos", "icono": "pi-plus-circle", "color": "#6B7280", "tipo": "ingreso" },
]


def crear_categorias_predefinidas(id_usuario: int, sesion: Session):
    """
    Crea las categorías predefinidas para un nuevo usuario.
    Se llama automáticamente al registrarse.
    """
    for datos_categoria in CATEGORIAS_PREDEFINIDAS:
        categoria = Categoria(
            nombre=datos_categoria["nombre"],
            icono=datos_categoria["icono"],
            color=datos_categoria["color"],
            tipo=datos_categoria["tipo"],
            id_usuario=id_usuario
        )
        sesion.add(categoria)
    sesion.commit()


def obtener_usuario_actual(
    token: str = Depends(oauth2_esquema),
    sesion: Session = Depends(obtener_sesion)
) -> Usuario:
    """
    Dependencia que extrae y valida el usuario autenticado desde el token JWT.
    """
    from app.core.seguridad import decodificar_token

    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodificar_token(token)
    if payload is None:
        raise credenciales_exception

    email: str = payload.get("sub")
    if email is None:
        raise credenciales_exception

    usuario = sesion.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credenciales_exception

    return usuario


@enrutador.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de nuevo usuario"
)
def registrar_usuario(
    datos: UsuarioCrear,
    sesion: Session = Depends(obtener_sesion)
):
    """
    Registra un nuevo usuario y crea sus categorías predefinidas.
    """
    usuario_existente = sesion.query(Usuario).filter(
        Usuario.email == datos.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        contrasena_hash=obtener_hash_contraseña(datos.contrasena),
        moneda=datos.moneda,
        zona_horaria=datos.zona_horaria
    )

    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)

    # Crea las categorías predefinidas para el nuevo usuario
    crear_categorias_predefinidas(nuevo_usuario.id, sesion)

    return nuevo_usuario


@enrutador.post(
    "/token",
    response_model=TokenAcceso,
    summary="Login y obtención de token JWT"
)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    sesion: Session = Depends(obtener_sesion)
):
    usuario = sesion.query(Usuario).filter(
        Usuario.email == formulario.username
    ).first()

    if not usuario or not verificar_contraseña(formulario.password, usuario.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario inactiva"
        )

    # Genera ambos tokens
    token_acceso = crear_token_acceso(datos={"sub": usuario.email})
    refresh_token = crear_refresh_token(datos={"sub": usuario.email})

    return {
        "access_token": token_acceso,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@enrutador.post(
    "/refresh",
    response_model=TokenAcceso,
    summary="Renovar token de acceso"
)
def renovar_token(
    datos: RefreshToken,
    sesion: Session = Depends(obtener_sesion)
):
    """
    Renueva el token de acceso usando el refresh token.
    Verifica que el refresh token sea válido y de tipo 'refresh'.
    """
    payload = decodificar_token(datos.refresh_token)

    if not payload or payload.get("tipo") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado"
        )

    email = payload.get("sub")
    usuario = sesion.query(Usuario).filter(Usuario.email == email).first()

    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )

    # Genera nuevos tokens
    nuevo_token_acceso = crear_token_acceso(datos={"sub": email})
    nuevo_refresh_token = crear_refresh_token(datos={"sub": email})

    return {
        "access_token": nuevo_token_acceso,
        "refresh_token": nuevo_refresh_token,
        "token_type": "bearer"
    }