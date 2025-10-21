from fastmcp import FastMCP
from pydantic import BaseModel
from fastapi import HTTPException, status
from auth import sign_in, get_current_user
from fastmcp.server.dependencies import get_http_headers

app = FastMCP("MCP Seguro")

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


@app.tool
async def iniciar_sesion(email: str, password: str) -> Token:
    """Inicia sesión y devuelve un token de acceso."""
    token_str = await sign_in(email, password)
    return Token(access_token=token_str, token_type="bearer")

@app.tool
def buscar_noticias(query: str, limit: int = 10):
    """Busca noticias sobre un tema específico.

    Args:
        query: El tema a buscar.
        limit: El número máximo de resultados a devolver.
    """
    print(f"Buscando {limit} noticias sobre '{query}'...")
    return [f"Noticia {i+1} sobre {query}" for i in range(limit)]

@app.tool
async def obtener_perfil_usuario() -> UserProfile:
    """Obtiene el perfil del usuario autenticado leyendo el token del header."""
    auth_header = get_http_headers().get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el header Authorization con el token Bearer",
        )

    token = auth_header.split(" ")[1]
    current_user = await get_current_user(token)

    user_id = current_user.get("sub")
    email = current_user.get("email", f"{user_id}@example.com")

    return UserProfile(
        user_id=user_id,
        username=f"user_{user_id[:6]}",
        email=email,
        is_active=True,
    )

@app.tool
def dividir(a: float, b: float) -> float:
    """Divide dos números. Falla si el divisor es cero."""
    print(f"Intentando dividir {a} / {b}...")
    if b == 0:
        raise ValueError("No se puede dividir por cero.")
    return a / b


if __name__ == "__main__":
    app.run()
    # app.run(transport="http", host="127.0.0.1", port=8000)