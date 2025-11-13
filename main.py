from typing import List
from fastmcp import FastMCP
from pydantic import BaseModel
from fastapi import HTTPException, status
from auth import sign_in, get_current_user, supabase
from fastmcp.server.dependencies import get_http_headers

app = FastMCP("MCP con Herramientas Stateful y Persistentes")

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str

class Session(BaseModel):
    session_id: str

class CartItem(BaseModel):
    item: str
    cantidad: int

class Cart(BaseModel):
    session_id: str
    items: List[CartItem]


@app.tool
def crear_carrito() -> Session:
    """
    Crea una nueva sesión de compra persistente en Supabase y devuelve un ID de sesión.
    """
    try:
        response = supabase.table("sessions").insert({"state": {"items": []}}).execute()
        
        if response.data:
            session_id = response.data[0]['id']
            print(f"Nueva sesión de carrito creada en Supabase: {session_id}")
            return Session(session_id=session_id)
        else:
            raise HTTPException(status_code=500, detail="No se pudo crear la sesión en la base de datos.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


@app.tool
def agregar_al_carrito(session_id: str, item: str, cantidad: int) -> Cart:
    """
    Agrega un item a un carrito de compras, actualizando el estado en Supabase.
    """
    try:
        response = supabase.table("sessions").select("state").eq("id", session_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"ID de sesión '{session_id}' no encontrado.")
        
        current_state = response.data[0]['state']
        cart_items = current_state.get("items", [])
        
        found = False
        for cart_item in cart_items:
            if cart_item["item"] == item:
                cart_item["cantidad"] += cantidad
                found = True
                break
        if not found:
            cart_items.append({"item": item, "cantidad": cantidad})
            
        new_state = {"items": cart_items}
        update_response = supabase.table("sessions").update({"state": new_state}).eq("id", session_id).execute()

        if not update_response.data:
            raise HTTPException(status_code=500, detail="No se pudo actualizar el carrito en la base de datos.")

        print(f"Item agregado al carrito {session_id}: {cantidad}x {item}")
        return Cart(session_id=session_id, items=[CartItem(**i) for i in cart_items])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


@app.tool
def ver_carrito(session_id: str) -> Cart:
    """
    Devuelve el contenido de un carrito consultando su estado en Supabase.
    """
    try:
        response = supabase.table("sessions").select("state").eq("id", session_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"ID de sesión '{session_id}' no encontrado.")
            
        current_state = response.data[0]['state']
        cart_items = current_state.get("items", [])
        print(f"Viendo carrito {session_id} desde Supabase")
        return Cart(session_id=session_id, items=[CartItem(**i) for i in cart_items])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


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
    # app.run()
    app.run(transport="http", host="127.0.0.1", port=8000)