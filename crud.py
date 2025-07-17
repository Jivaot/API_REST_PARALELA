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

# -------------------- INSERCIÓN --------------------

async def insert_one(
    conn: asyncpg.Pool,
    table: str,
    data: Dict[str, Any],
    returning: str = "*",
) -> Dict[str, Any]:
    """
    Inserta un registro en la tabla dada y devuelve la fila retornada.
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
    values = list(data.values())
    query = (
        f"INSERT INTO {table} ({columns}) "
        f"VALUES ({placeholders}) "
        f"RETURNING {returning}"
    )
    row = await conn.fetchrow(query, *values)
    return dict(row)

# ------------------ ACTUALIZACIÓN ------------------

async def update_by_id(
    conn: asyncpg.Pool,
    table: str,
    id: int,
    data: Dict[str, Any],
    returning: str = "*",
) -> Optional[Dict[str, Any]]:
    """
    Actualiza el registro con el id dado y devuelve la fila actualizada.
    """
    set_clause = ", ".join(f"{key} = ${i+2}" for i, key in enumerate(data))
    values = [id] + list(data.values())
    query = (
        f"UPDATE {table} SET {set_clause} "
        f"WHERE id = $1 "
        f"RETURNING {returning}"
    )
    row = await conn.fetchrow(query, *values)
    return dict(row) if row else None

# ------------------- ELIMINACIÓN -------------------

async def delete_by_id(conn: asyncpg.Pool, table: str, id: int) -> str:
    """
    Elimina el registro con el id dado y devuelve el resultado del execute.
    """
    query = f"DELETE FROM {table} WHERE id = $1"
    return await conn.execute(query, id)
