from pydantic import BaseModel, Field

class CodeInfo(BaseModel):
    code: str = Field(..., description="Código del elemento", example="001")
    name: str = Field(..., description="Nombre descriptivo del elemento", example="Chile")

    class Config:
        # esto aplica un ejemplo completo al schema
        json_schema_extra = {
            "example": {
                "code": "001",
                "name": "Chile"
            }
        }


class CountStat(BaseModel):
    count: int = Field(..., description="Cantidad absoluta", example=42)
    percentage: float = Field(..., description="Porcentaje representado", example=12.5)

class AgeStat(BaseModel):
    min: float = Field(..., description="Edad mínima", example=18.0)
    max: float = Field(..., description="Edad máxima", example=99.0)
    mean: float = Field(..., description="Edad promedio", example=45.35)
    stddev: float = Field(..., description="Desviación estándar de la edad", example=12.75)

class ProblemDetail(BaseModel):
    type: str = Field(..., example="https://example.com/")
    title: str = Field(..., example="Error")
    status: int = Field(..., example=500)
    detail: str = Field(..., example="Ocurrió un error inesperado")
    instance: str = Field(..., example="https://example.com/")
    properties: dict = Field(default_factory=dict)

