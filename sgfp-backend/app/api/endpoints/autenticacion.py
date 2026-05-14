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