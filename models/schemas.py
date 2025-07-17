from pydantic import BaseModel, Field

from pydantic import BaseModel, Field

class CodeInfo(BaseModel):
    code: str = Field(..., example="001")
    name: str = Field(..., example="Chile")

    class Config:
        # esto aplica un ejemplo completo al schema
        schema_extra = {
            "example": {
                "code": "001",
                "name": "Chile"
            }
        }


class CountStat(BaseModel):
    count: int = Field(..., example=45)
    percentage: float = Field(..., example=12.5)

class AgeStat(BaseModel):
    min: int = Field(..., example=12)
    max: int = Field(..., example=89)
    avg: float = Field(..., example=32.5)

class ProblemDetail(BaseModel):
    type: str = Field(..., example="https://example.com/")
    title: str = Field(..., example="Error")
    status: int = Field(..., example=500)
    detail: str = Field(..., example="Ocurrió un error inesperado")
    instance: str = Field(..., example="https://example.com/")
    additionalProp1: str = Field(..., example="string")
    additionalProp2: str = Field(..., example="string")
    additionalProp3: str = Field(..., example="string")

