# database.py

import asyncpg
from typing import Optional

class Database:
    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        # Crea un pool de conexiones al arrancar
        self._pool = await asyncpg.create_pool(
            host="159.223.200.213",
            port=5432,
            user="isekai",
            password="Fr9tL28mQxD7vKcp",
            database="isekaidb",
            min_size=1,
            max_size=5,
        )

    async def disconnect(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    def get_connection(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("Conexión a BD no inicializada")
        return self._pool

# Instancia global que importas en main.py y en tus routers
db = Database()
