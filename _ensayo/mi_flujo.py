"""Flujo de exportaciones con catálogo: extrae exportaciones, valida filas y total, y guarda con la fecha del corte.
Integrantes: Equipo 5.3
Fuente: datos/exportaciones.csv (archivo de EJEMPLO sintético de la clase)
SI FALLA: si la fuente no llega o cambia de formato, el flujo se detiene con ERROR en flujo.log y código de salida 1. Avisar al responsable de datos del área (o al docente en clase)."""
import logging, sys
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_ENTRADA    = "datos/exportaciones.csv"
SALIDA          = f"salida/mi_flujo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS = 7
TOTAL_ESPERADO  = 8679.13

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("mi_flujo")

# ---------- 2 · LAS TRES FUNCIONES (cada una con su docstring) ----------
def extraer():
    """Lee el CSV de exportaciones y devuelve un DataFrame."""
    tabla = pd.read_csv(RUTA_ENTRADA)
    log.info("extraidas %d filas", len(tabla))
    return tabla

def transformar(tabla):
    """Valida número de filas y total esperado; devuelve la tabla sin cambios."""
    if len(tabla) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(tabla)}")
    total = round(tabla["monto_mm_usd"].sum(), 2)
    if abs(total - TOTAL_ESPERADO) > 0.01:
        raise ValueError(f"el total cambio: esperaba {TOTAL_ESPERADO} y salio {total}")
    return tabla

def cargar(tabla):
    """Guarda la tabla en salida/ con la fecha del corte en el nombre."""
    import os; os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False)
    log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        cargar(transformar(extraer())); log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error); sys.exit(1)
