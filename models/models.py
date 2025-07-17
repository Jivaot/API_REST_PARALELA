# models.py
from pydantic import BaseModel, Field

# GENDERS
class Gender(BaseModel):
    id: int
    name: str

class CodeInfo(BaseModel):
    code: str
    name: str

class GenderCreate(BaseModel):
    name: str

# SPECIES
class Species(BaseModel):
    id: int
    name: str

class SpeciesCreate(BaseModel):
    name: str

# STRATA
class Stratum(BaseModel):
    id: int
    name: str

class StratumCreate(BaseModel):
    name: str

# PERSONS
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
