from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from src.tools.db_tools import list_tables, get_schema, execute_sql
from src.agente.formatter import VisualResponse
from langgraph.prebuilt import ToolNode
from src.agente.state import AgentState
import os
from dotenv import load_dotenv

# 1. Cargar Entorno
load_dotenv('accesos.env')
api_key = os.getenv("OPENAI_API_KEY")

# 2. Instanciar Modelos
# Modelo de lenguaje principal
llm = ChatOpenAI(model='gpt-4o', temperature=50, api_key=api_key)
# Modelo estructurado para la respuesta final
structured_llm = llm.with_structured_output(VisualResponse)

# 3. Definir Herramientas
tools = [list_tables, get_schema, execute_sql]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# 4. Funciones de los Nodos
def call_model(state: AgentState):
    """Nodo principal del agente."""
    messages = state["messages"]
    # Si es el primer mensaje, le damos contexto de analista SQL
    if len(messages) == 1:
        messages = [{"role": "system",
                     "content": "Eres un experto analista SQL. Responde siempre en español."}] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def format_final_answer(state: AgentState):
    """Nodo final que genera la respuesta estructurada para la UI."""
    messages = state["messages"]
    system_instruction = (
        "Resume los hallazgos anteriores en el formato estructurado VisualResponse. "
        "Si no hay datos para graficar, deja 'data': [] y usa visualization_type: 'table'."
    )
    response = structured_llm.invoke(messages + [{"role": "system", "content": system_instruction}])
    return {"final_structured_response": response}

# 5. Lógica de Navegación
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "formatter"


# 6. Construcción del Grafo, vía un StateGraph
workflow = StateGraph(AgentState)

## Agregar los nodos:
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_node("formatter", format_final_answer)

# Establecer el punto de entrada
workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "formatter": "formatter"
    }
)

workflow.add_edge("tools", "agent")
workflow.add_edge("formatter", END)

app = workflow.compile()