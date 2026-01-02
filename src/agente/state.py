from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from src.agente.formatter import VisualResponse # Importa tu modelo
'''
    Notas:
        El uso de un estado es relevante para un agente basado en LangGraph.
        El estado, contiene todo lo que el agente necesita para razonar.
        En este caso, el estado contiene el historial de mensajes.
        Además, se agrega un campo para la respuesta formateada final.
'''
class AgentState(TypedDict):
    # 'messages' usa Annotated y add_messages para ir acumulando el historial, y así razonar correctamente.
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # Vista estructurada final para el usuario
    final_structured_response: VisualResponse