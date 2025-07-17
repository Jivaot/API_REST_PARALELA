not_found = {
    "content": {
        "application/problem+json": {
            "example": {
                "type": "https://example.com/",
                "title": "Error",
                "status": 404,
                "detail": "No hay información de géneros disponible",
                "instance": "https://example.com/",
            }
        }
    }
}

internal_error = {
    "content": {
        "application/problem+json": {
            "example": {
                "type": "https://example.com/",
                "title": "Error",
                "status": 500,
                "detail": "Ocurrió un error inesperado",
                "instance": "https://example.com/",
            }
        }
    }
}
