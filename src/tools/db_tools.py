## Importe de dependencias necesarias
from pathlib import Path
from langchain_community.utilities import SQLDatabase # Lectura y manipulación de bases de datos SQL
from langchain_core.tools import tool # Incorporación de herramientas para el agente

## Paso 1:
    # Generación de la conexión de la base de datos (en este caso, se usa se ejecuta el main.py de data antes de este paso)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "Chinook.db"

if not DB_PATH.exists():
    # Tip: Es útil para el README mencionar que deben ejecutar primero el script de descarga
    raise FileNotFoundError(f"Base de datos no encontrada en: {DB_PATH}. Ejecuta el script de descarga primero.")

# --- INICIALIZACIÓN GLOBAL DEL OBJETO DB ---
# Lo definimos aquí para que todas las herramientas lo compartan
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH.as_posix()}")

## Paso 2:
    # Definición de la herramienta para consultar la base de datos SQL
    # La idea es que el agente sea capaz de leer y consultar la base de datos

@tool
def list_tables():
    '''
    Le da la capacidad al agente de listar las tablas de la base de datos SQL
    Returns:
        str: Lista de tablas en la base de datos SQL
    '''
    return db.get_usable_table_names()

@tool
def get_schema(table_names: str):
    '''
    Le da la capacidad al agente de obtener el esquema de la base de datos SQL
    Returns:
        str: Esquema de la base de datos SQL
    '''
    return db.get_table_info(table_names.split(","))

@tool
def execute_sql(query: str):
    '''
    Le da la capacidad al agente de ejecutar consultas SQL en la base de datos
    Args:
        query (str): Consulta SQL a ejecutar
    Returns:
        str: Resultados de la consulta SQL
    '''
    try:
        return db.run(query)
    except Exception as e:
        # Manejo de errores en la ejecución de la consulta SQL
        return f"Error: {str(e)}"