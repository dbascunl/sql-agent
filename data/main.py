## Dependencias
import requests
from pathlib import Path

def main() -> None:
    '''
    Descarga la base de datos Chinook en formato SQLite y la guarda como Chinook.db
    Si el archivo ya existe, no realiza la descarga nuevamente.
    '''
    url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
    output_path = Path("Chinook.db")

    if output_path.exists():
        print("La base de datos Chinook.db ya existe.")
        return
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with output_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # evita chunks vacíos
                    f.write(chunk)
        print("Descarga completada: Chinook.db")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la base de datos: {e}")

if __name__ == "__main__":
    main()
