from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal, Optional

'''
    Nota:
    Este modelo de datos está diseñado para estructurar la respuesta de un agente.
    Esto es útil para asegurar que la salida del agente sea consistente y fácil de interpretar.
'''

class VisualResponse(BaseModel):
    analysis: str = Field(description="Un resumen detallado en español de los hallazgos.")
    sql_query: str = Field(description="La consulta SQL final que generó estos datos.")
    visualization_type: Literal["table", "bar", "line", "pie"] = Field(
        description="El tipo de gráfico más adecuado para representar estos datos."
    )
    data: Optional[List[Dict[str, Any]]] = Field(
        default=[],
        description="Lista de diccionarios con los resultados de la consulta SQL."
    )
    columns: Optional[List[str]] = Field(
        default=None,
        description="Orden de columnas para la tabla (si aplica)."
    )