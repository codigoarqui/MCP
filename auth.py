from supabase import create_client, Client
from fastapi import HTTPException, status
from jose import jwt, JWTError
from config import SUPABASE_URL, SUPABASE_ANON_KEY
import requests

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

JWKS_URL = "https://cilduzxagslwmgqydwik.supabase.co/auth/v1/.well-known/jwks.json"

def get_jwk_for_kid(kid: str):
    jwks = requests.get(JWKS_URL).json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se encontró la clave pública para este token",
    )


async def sign_in(email: str, password: str) -> str:
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            return response.session.access_token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al autenticar: {e}",
        )

async def get_current_user(token: str):
    try:
        header = jwt.get_unverified_header(token)
        jwk = get_jwk_for_kid(header["kid"])
        payload = jwt.decode(
            token,
            jwk,
            algorithms=[header["alg"]],
            audience="authenticated",
            issuer="https://cilduzxagslwmgqydwik.supabase.co/auth/v1"
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return payload
    except JWTError as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o expirado",
        )