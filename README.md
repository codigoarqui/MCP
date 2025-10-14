# Catálogo de Herramientas MCP con FastMCP

Este proyecto demuestra cómo construir un servidor de herramientas compatible con el **Multimodal Communication Protocol (MCP)** de una manera rápida y profesional utilizando la librería `fastmcp`.

El servidor expone un catálogo con 3 herramientas variadas para mostrar diferentes funcionalidades:

1.  `buscar_noticias`: Una herramienta con parámetros opcionales y valores por defecto.
2.  `obtener_perfil_usuario`: Una herramienta que devuelve un objeto de datos complejo (un modelo Pydantic).
3.  `dividir`: Una herramienta diseñada para demostrar el manejo automático de errores.

## Cómo Empezar

### 1. Prerrequisitos

-   Python 3.8+
-   Node.js 18+ (para usar la herramienta de inspección)

### 2. (Recomendado) Crear y Activar un Entorno Virtual

```bash
python3 -m venv venv
venv\Scripts\activate
```

**Para macOS y Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalación

Con tu entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

## Cómo Probarlo

La mejor forma de probar el servidor es con `mcp-inspector`.

1.  Con tu servidor corriendo, abre una **segunda terminal**.
2.  Ejecuta el inspector apuntando a la URL de tu servidor:

```bash
npx @modelcontextprotocol/inspector
```