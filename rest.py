from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
import asyncpg

app = FastAPI(title="Isekai API Replica", description="Réplica completa del API REST", version="1.0.0")

# Conexión global
conn_ref = None

async def connect_to_db():
    global conn_ref
    if conn_ref is None:
        conn_ref = await asyncpg.connect(
            user="isekai",
            password="Fr9tL28mQxD7vKcp",
            database="isekaidb",
            host="159.223.200.213",
            port=5432
        )
    return conn_ref

def get_conn():
    return conn_ref

# Models
class Gender(BaseModel):
    id: int
    name: str

class GenderCreate(BaseModel):
    name: str

class Species(BaseModel):
    id: int
    name: str

class SpeciesCreate(BaseModel):
    name: str

class Stratum(BaseModel):
    id: int
    name: str

class StratumCreate(BaseModel):
    name: str

class Person(BaseModel):
    id: int
    name: str
    age: int
    gender_id: int
    species_id: int
    stratum_id: int

class PersonCreate(BaseModel):
    name: str
    age: int
    gender_id: int
    species_id: int
    stratum_id: int

# Utils
async def get_all(conn, table: str):
    return await conn.fetch(f"SELECT * FROM {table}")

async def get_by_id(conn, table: str, id: int):
    return await conn.fetchrow(f"SELECT * FROM {table} WHERE id = $1", id)

async def delete_by_id(conn, table: str, id: int):
    return await conn.execute(f"DELETE FROM {table} WHERE id = $1", id)

# Routers
@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.get("/genders", response_model=List[Gender], tags=["Genders"])
async def list_genders(conn=Depends(get_conn)):
    return [dict(r) for r in await get_all(conn, "genders")]

@app.get("/genders/{id}", response_model=Gender, tags=["Genders"])
async def get_gender(id: int, conn=Depends(get_conn)):
    row = await get_by_id(conn, "genders", id)
    if not row:
        raise HTTPException(404, "Gender not found")
    return dict(row)

@app.get("/species", response_model=List[Species], tags=["Species"])
async def list_species(conn=Depends(get_conn)):
    return [dict(r) for r in await get_all(conn, "species")]

@app.get("/species/{id}", response_model=Species, tags=["Species"])
async def get_species(id: int, conn=Depends(get_conn)):
    row = await get_by_id(conn, "species", id)
    if not row:
        raise HTTPException(404, "Species not found")
    return dict(row)

@app.get("/strata", response_model=List[Stratum], tags=["Strata"])
async def list_strata(conn=Depends(get_conn)):
    return [dict(r) for r in await get_all(conn, "strata")]

@app.get("/strata/{id}", response_model=Stratum, tags=["Strata"])
async def get_stratum(id: int, conn=Depends(get_conn)):
    row = await get_by_id(conn, "strata", id)
    if not row:
        raise HTTPException(404, "Stratum not found")
    return dict(row)

@app.get("/persons", response_model=List[Person], tags=["Persons"])
async def list_persons(conn=Depends(get_conn)):
    return [dict(r) for r in await get_all(conn, "persons")]

@app.get("/persons/{id}", response_model=Person, tags=["Persons"])
async def get_person(id: int, conn=Depends(get_conn)):
    row = await get_by_id(conn, "persons", id)
    if not row:
        raise HTTPException(404, "Person not found")
    return dict(row)

@app.post("/persons", response_model=Person, status_code=status.HTTP_201_CREATED, tags=["Persons"])
async def create_person(person: PersonCreate, conn=Depends(get_conn)):
    query = """
        INSERT INTO persons (name, age, gender_id, species_id, stratum_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """
    result = await conn.fetchrow(query, person.name, person.age, person.gender_id, person.species_id, person.stratum_id)
    return dict(result)

@app.delete("/persons/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Persons"])
async def delete_person(id: int, conn=Depends(get_conn)):
    result = await delete_by_id(conn, "persons", id)
    if result == "DELETE 0":
        raise HTTPException(404, "Person not found")
    return