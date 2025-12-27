# sql-agent

Este proyecto contiene el desarrollo de un agente capaz de interactuar con un motor de base de datos SQL (SQLite), utilizando lenguaje natural. Este sistema utiliza un razonador (LLM) con la capacidad de auto-correción de errores, generar salida de datos estructurada, con el objetivo de facilitar preguntas concretas de los usuarios.

## Stack utilizado

* **Orquestación** : LangChain & LangGraph
* **LLM** : OpenAI (GPT-4o)
* **Base de Datos**: SQLite - Dataset (Chinook)
* **Visualización** : Plotly

## Diseño del Agente

El agente sigue un flujo de cadena de pensamiento (CoT), es decir, se provee una lógica de razonamiento, con el objetivo de dar un sólo resultado.

1. **Herramientas de búsqueda** : Lista de tablas para entender en contexto global de la base de datos relacional.
2. **Pensamiento**: Obtiene desde los `Create Table` de las tablas relevantes a la pregunta del usuario.
3. **Escritura de consulta** : Crea una consulta en SQL basada el motor de la base datos, en este caso SQLite.
4. **Ejecución y Validación**: Ejecuta la consulta, con dos casos probables (acierto) y, caso de error (error) entra un bucle de correción.
5. **Salida**: Entrega los resultados de la consulta del humano en Json estructurado y/o una visualización en caso de haberla solicitado.

## Instalación y uso del agente

1. Clonar el repositorio: `git clone https://github.com/dbascunl/sql-agent.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables de entorno: Crear un archivo `.env` con tu `OPENAI_API_KEY`.

## Dudas, consultas & contribuciones

* Puedes escribirme a mi correo personal dbascunl@gmail.com
