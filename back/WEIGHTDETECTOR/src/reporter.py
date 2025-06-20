# reporter.py
import csv
from datetime import datetime
from pathlib import Path


def generar_reporte(pesos: list[str]) -> Path:
    """
    Genera un reporte CSV con los últimos 10 pesos.
    Se guarda en src/Reportes/ con nombre único basado en fecha y hora.
    Incluye columnas: índice, peso, fecha/hora de registro.
    """
    if not pesos:
        raise ValueError("La lista de pesos está vacía")

    # Preparar carpeta de destino
    carpeta_reportes = Path(__file__).parent / "Reportes"
    carpeta_reportes.mkdir(parents=True, exist_ok=True)

    # Nombre único para el archivo
    nombre_archivo = f"reporte_pesos_{datetime.now():%Y%m%d_%H%M%S}.csv"
    ruta_archivo = carpeta_reportes / nombre_archivo

    # Obtener los 10 últimos con la marca de tiempo actual
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ultimos = pesos[-10:]

    with ruta_archivo.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Peso (Kg)", "Fecha"])
        for i, peso in enumerate(ultimos, 1):
            writer.writerow([i, peso, ahora])

    return ruta_archivo
