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

async def get_species_pk(code: str) -> Optional[int]:
    """Obtiene el pk de una especie por su código."""
    pool = db.get_connection()
    return await pool.fetchval("SELECT pk FROM species WHERE code = $1", code)

async def get_strata_pk(code: str) -> Optional[int]:
    """Obtiene el pk de un estrato por su código."""
    pool = db.get_connection()
    # Convertir a int si es posible, ya que los códigos de estrato son numéricos
    try:
        code_int = int(code)
        return await pool.fetchval("SELECT pk FROM strata WHERE code = $1", code_int)
    except ValueError:
        return None

async def get_gender_pk(code: str) -> Optional[int]:
    """Obtiene el pk de un género por su código."""
    pool = db.get_connection()
    return await pool.fetchval("SELECT pk FROM genders WHERE code = $1", code)

@router.get(
    "/count",
    response_model=CountStat,
    summary="Obtener estadística de conteo",
    description="Retorna la cantidad y porcentaje de individuos para los filtros dados",
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
        400: {
            "description": "Parámetros inválidos",
            "content": {
                "application/problem+json": {
                    "example": not_found["content"]["application/problem+json"]["example"]
                }
            }
        },
    },
)
async def count_stats(
    speciesCode: Optional[str] = Query(None, alias="speciesCode", description="Código de especie", example="HU"),
    strataCode:  Optional[str] = Query(None, alias="strataCode",  description="Código de estrato", example=0),
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

        # 2) Construir WHERE dinámico con conversión de códigos a IDs
        conditions = []
        args = []
        arg_count = 0
        
        if speciesCode is not None:
            species_pk = await get_species_pk(speciesCode)
            if species_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"species_fk = ${arg_count}")
            args.append(species_pk)
            
        if strataCode is not None:
            strata_pk = await get_strata_pk(strataCode)
            if strata_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"strata_fk = ${arg_count}")
            args.append(strata_pk)
            
        if genderCode is not None:
            gender_pk = await get_gender_pk(genderCode)
            if gender_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"gender_fk = ${arg_count}")
            args.append(gender_pk)

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

        # Porcentaje como valor entre 0 y 1, redondeado a 6 decimales
        percentage = round(count / total, 6)

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
    description="Retorna el valor mínimo, máximo y promedio de edad para los filtros dados",
    responses={
        200: {
            "description": "Estadística de edad obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {"min": 18.0, "max": 99.0, "mean": 45.35, "stddev": 12.75}
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
        400: {
            "description": "Parámetros inválidos",
            "content": {
                "application/problem+json": {
                    "example": not_found["content"]["application/problem+json"]["example"]
                }
            }
        },
    },
)
async def age_stats(
    speciesCode: Optional[str] = Query(None, alias="speciesCode", description="Código de especie", example="HU"),
    strataCode:  Optional[str] = Query(None, alias="strataCode",  description="Código de estrato", example=5),
    genderCode:  Optional[str] = Query(None, alias="genderCode",  description="Código de género", example="M"),
):
    """
    Calcula mínimo, máximo, promedio y desviación estándar de edad directamente en la base de datos.
    """
    pool = db.get_connection()
    try:
        # Construir SELECT dinámico con conversión de códigos a IDs
        base_sql = (
            "SELECT "
            "MIN(date_part('year', age(birthdate)))::float AS min, "
            "MAX(date_part('year', age(birthdate)))::float AS max, "
            "AVG(date_part('year', age(birthdate)))::float AS mean, "
            "STDDEV(date_part('year', age(birthdate)))::float AS stddev "
            "FROM persons"
        )

        conditions = []
        args = []
        arg_count = 0
        
        if speciesCode is not None:
            species_pk = await get_species_pk(speciesCode)
            if species_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"species_fk = ${arg_count}")
            args.append(species_pk)
            
        if strataCode is not None:
            strata_pk = await get_strata_pk(strataCode)
            if strata_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"strata_fk = ${arg_count}")
            args.append(strata_pk)
            
        if genderCode is not None:
            gender_pk = await get_gender_pk(genderCode)
            if gender_pk is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=not_found["content"]["application/problem+json"]["example"],
                    media_type="application/problem+json",
                )
            arg_count += 1
            conditions.append(f"gender_fk = ${arg_count}")
            args.append(gender_pk)

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

        # Redondeamos a 4 decimales para coincidir con la API del profesor
        return {
            "min": round(row["min"], 4),
            "max": round(row["max"], 4),
            "mean": round(row["mean"], 4),
            "stddev": round(row["stddev"], 4) if row["stddev"] is not None else 0.0,
        }

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=internal_error["content"]["application/problem+json"]["example"],
            media_type="application/problem+json",
        )
