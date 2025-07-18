# crud.py

from typing import Any, Dict, List, Optional
import asyncpg

async def get_all_persons(conn: asyncpg.Pool, table: str) -> List[Dict[str, Any]]:
    """
    Recupera todas las filas de la tabla `persons`, mapeando fields a
    species, strata, gender y calculando age en años.
    """
    query = (
        f"SELECT "
        f"species_fl  AS species, "
        f"strata_fl   AS strata, "
        f"gender_fl   AS gender, "
        f"date_part('year', age(birthdate))::int AS age "
        f"FROM {table}"
    )
    rows = await conn.fetch(query)
    return [dict(row) for row in rows]

# -------------------- LECTURA GENERAL --------------------

async def get_all(conn: asyncpg.Pool, table: str) -> List[Dict[str, Any]]:
    """
    Recupera todas las filas de cualquier tabla (ordenadas por id).
    """
    query = f"SELECT * FROM {table} ORDER BY id"
    rows = await conn.fetch(query)
    return [dict(row) for row in rows]

async def get_by_id(conn: asyncpg.Pool, table: str, id: int) -> Optional[Dict[str, Any]]:
    """
    Recupera una fila por su id de cualquier tabla.
    """
    query = f"SELECT * FROM {table} WHERE id = $1"
    row = await conn.fetchrow(query, id)
    return dict(row) if row else None
