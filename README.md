# Un API de otro mundo

API desarrollada para el trabajo de la asignatura **Computación Paralela y Distribuida** de la UTEM (semestre de otoño 2025). Esta API simula un mundo de fantasía (isekai) y permite consultar información y estadísticas sobre especies, géneros y estratos sociales.

## Tecnologías utilizadas
- Python 3.10+
- FastAPI
- asyncpg
- PostgreSQL (remoto)
- Uvicorn

## Instalación

   
1. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta el servidor**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
3 **la pagina se aloja**
 ```  http://127.0.0.1:8000/docs#/
  ```
## Endpoints principales

- `GET /v1/info/genders` — Lista de géneros
- `GET /v1/info/species` — Lista de especies
- `GET /v1/info/strata` — Lista de estratos sociales
- `GET /v1/stats/count` — Estadísticas de conteo (parámetros: `speciesCode`, `strataCode`, `genderCode`)
- `GET /v1/stats/age` — Estadísticas de edad (parámetros: `speciesCode`, `strataCode`, `genderCode`)



**Autores:** [Javier Fernandez,Glenn Lanyonn]

**Licencia:** CC0 1.0 Universal 