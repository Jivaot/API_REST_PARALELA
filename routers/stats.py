# routers/stats.py

from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
from database import db
from models.schemas import CountStat, AgeStat
from utils.errors import not_found, internal_error

router = APIRouter(
    prefix="/v1/stats",
    tags=["Estadísticas"],
)

@router.get(
    "/count",
    response_model=CountStat,
    summary="Obtener estadística de conteo",
    description="Retorna la cantidad y el porcentaje de individuos para los filtros dados",
    responses={
        200: {
            "description": "Estadística de conteo obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {"count": 9192, "percentage": 0.009192}
                }
            }
        },
        404: {
            "description": "No hay datos disponibles para los filtros proporcionados",
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
async def count_stats(
    speciesCode: Optional[str] = Query(None, alias="speciesCode", description="Código de especie", example="HU"),
    strataCode:  Optional[str] = Query(None, alias="strataCode",  description="Código de estrato", example="0"),
    genderCode:  Optional[str] = Query(None, alias="genderCode",  description="Código de género", example="F"),
):
    """
    Calcula el conteo total y filtrado de la tabla `persons` usando SQL.
    """
    pool = db.get_connection()
    try:
        # 1) Total global
        total = await pool.fetchval("SELECT COUNT(*) FROM persons")
        if total == 0:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=not_found["content"]["application/problem+json"]["example"],
                media_type="application/problem+json",
            )

        # 2) Construir WHERE dinámico
        conditions = []
        args = []
        if speciesCode is not None:
            conditions.append(f"species_fl = ${len(args)+1}")
            args.append(speciesCode)
        if strataCode is not None:
            conditions.append(f"strata_fl = ${len(args)+1}")
            args.append(strataCode)
        if genderCode is not None:
            conditions.append(f"gender_fl = ${len(args)+1}")
            args.append(genderCode)

        # 3) Conteo filtrado
        if conditions:
            where_clause = " AND ".join(conditions)
            sql = f"SELECT COUNT(*) FROM persons WHERE {where_clause}"
            count = await pool.fetchval(sql, *args)
        else:
            count = total

        if count == 0:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=not_found["content"]["application/problem+json"]["example"],
                media_type="application/problem+json",
            )

        # 4) Porcentaje
        percentage = round((count / total) * 100, 6)

        return {"count": count, "percentage": percentage}

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=internal_error["content"]["application/problem+json"]["example"],
            media_type="application/problem+json",
        )


@router.get(
    "/age",
    response_model=AgeStat,
    summary="Obtener estadística de edad",
    description="Retorna mínimo, máximo y promedio de edad para los filtros dados",
    responses={
        200: {
            "description": "Estadística de edad obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {"min": 0, "max": 120, "avg": 65.4}
                }
            }
        },
        404: {
            "description": "No hay datos disponibles para los filtros proporcionados",
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
async def age_stats(
    speciesCode: Optional[str] = Query(None, alias="speciesCode", description="Código de especie", example="HU"),
    strataCode:  Optional[str] = Query(None, alias="strataCode",  description="Código de estrato", example="0"),
    genderCode:  Optional[str] = Query(None, alias="genderCode",  description="Código de género", example="F"),
):
    """
    Calcula mínimo, máximo y promedio de edad directamente en la base de datos.
    """
    pool = db.get_connection()
    try:
        # Construir SELECT dinámico
        base_sql = (
            "SELECT "
            "MIN(date_part('year', age(birthdate)))::int AS min, "
            "MAX(date_part('year', age(birthdate)))::int AS max, "
            "AVG(date_part('year', age(birthdate)))::float AS avg "
            "FROM persons"
        )

        conditions = []
        args = []
        if speciesCode is not None:
            conditions.append(f"species_fl = ${len(args)+1}")
            args.append(speciesCode)
        if strataCode is not None:
            conditions.append(f"strata_fl = ${len(args)+1}")
            args.append(strataCode)
        if genderCode is not None:
            conditions.append(f"gender_fl = ${len(args)+1}")
            args.append(genderCode)

        if conditions:
            where_clause = " AND ".join(conditions)
            sql = f"{base_sql} WHERE {where_clause}"
            row = await pool.fetchrow(sql, *args)
        else:
            row = await pool.fetchrow(base_sql)

        if not row or row["min"] is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=not_found["content"]["application/problem+json"]["example"],
                media_type="application/problem+json",
            )

        # El avg viene como float; redondeamos a 2 decimales
        return {
            "min": row["min"],
            "max": row["max"],
            "avg": round(row["avg"], 2),
        }

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=internal_error["content"]["application/problem+json"]["example"],
            media_type="application/problem+json",
        )
