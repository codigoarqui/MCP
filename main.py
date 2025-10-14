from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Literal
import uvicorn

app = FastMCP("Mi Catálogo de Herramientas Avanzado")


class UserProfile(BaseModel):
    """Representa un perfil de usuario estructurado."""
    user_id: str
    username: str
    email: str
    is_active: bool


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
def obtener_perfil_usuario(user_id: str) -> UserProfile:
    """Obtiene el perfil de un usuario basado en su ID."""
    print(f"Obteniendo perfil para el usuario '{user_id}'...")
    return UserProfile(
        user_id=user_id,
        username=f"user_{user_id}",
        email=f"{user_id}@example.com",
        is_active=True
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

