# routers/genders.py

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from database import db
from models.schemas import CodeInfo
from utils.errors import not_found, internal_error

router = APIRouter(
    prefix="/v1/info",
    tags=["Información base"],
)

TABLE = "genders"

@router.get(
    "/genders",
    response_model=list[CodeInfo],
    summary="Listar géneros disponibles",
    responses={
        200: {
            "description": "Listado de géneros obtenido exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {"code": "M", "name": "Masculino"},
                        {"code": "F", "name": "Femenino"}
                    ]
                }
            }
        },
        404: {
            "description": "No hay información de géneros disponible",
            "content": {
                "application/problem+json": {
                    "example": not_found["content"]["application/problem+json"]["example"]
                }
            }
        },
        500: {
            "description": "Error interno no manejado",
            "content": {
                "application/problem+json": {
                    "example": internal_error["content"]["application/problem+json"]["example"]
                }
            }
        },
    },
)
async def list_genders():
    """
    Retorna la lista de géneros (code, name) desde la tabla `genders`.
    Si no hay filas, devuelve 404; ante errores internos, devuelve 500.
    """
    conn = db.get_connection()
    try:
        rows = await conn.fetch(f"SELECT code, name FROM {TABLE} ORDER BY code")
        if not rows:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=not_found["content"]["application/problem+json"]["example"],
                media_type="application/problem+json",
            )
        return [{"code": row["code"], "name": row["name"]} for row in rows]
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=internal_error["content"]["application/problem+json"]["example"],
            media_type="application/problem+json",
        )
