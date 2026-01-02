import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
st.set_page_config(page_title="SQL Agent", layout="wide")

## Cargar el agente
try:
    from src.agente.sql_agente import app as agent_app
except Exception as e:
    st.error(f"Error al cargar el agente: {e}")
    st.stop()

## Interfaz de Usuario:
st.title("SQL Agent")   # Título de la aplicación
st.markdown("Realiza consultas a tu base de datos utilizando lenguaje natural") # Descripción

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "visual" in message:
            st.code(message["visual"].sql_query, language="sql")

# Chat Input
if prompt := st.chat_input("¿Qué quieres saber de tu base de datos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando base de datos..."):
            # Ejecutar el grafo de LangGraph
            inputs = {"messages": [("user", prompt)]}
            config = {"configurable": {"thread_id": "1"}}

            result = agent_app.invoke(inputs, config)

            # Extraer respuesta estructurada del nodo 'formatter'
            final_res = result.get("final_structured_response")

            if final_res:
                st.markdown(final_res.analysis)
                with st.expander("Ver consulta SQL ejecutada"):
                    st.code(final_res.sql_query, language="sql")

                # Guardar en historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_res.analysis,
                    "visual": final_res
                })
            else:
                st.error("No se pudo obtener una respuesta estructurada.")