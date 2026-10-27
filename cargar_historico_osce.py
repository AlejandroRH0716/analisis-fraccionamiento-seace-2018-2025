import os
import sys
import urllib
import pandas as pd
from sqlalchemy import create_engine

servidor = r"PC\SQLEXPRESS"
base_datos = "OSCE_Auditoria"

cadena_conexion = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={servidor};"
    f"DATABASE={base_datos};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(cadena_conexion)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

dtype_dict = {
    "ruc_entidad": str,
    "nro_de_orden": str,
    "ruc_contratista": str,
}

columnas_fecha = [
    "fecha_registro",
    "fecha_de_emision",
    "fecha_compromiso_presupuestal",
    "fecha_de_notificacion"
]

directorio_raiz = os.path.dirname(os.path.abspath(__file__))

carpetas_anios = sorted([
    c for c in os.listdir(directorio_raiz) 
    if os.path.isdir(os.path.join(directorio_raiz, c)) and c.isdigit() and len(c) == 4
])

if not carpetas_anios:
    print("Error: No se encontraron subcarpetas de años en el directorio:")
    print(directorio_raiz)
    sys.exit(1)

print(f"Directorio de trabajo: {directorio_raiz}")
print(f"Carpetas de años detectadas para procesamiento: {carpetas_anios}\n")

total_archivos_procesados = 0
total_filas_insertadas = 0

for anio in carpetas_anios:
    ruta_anio = os.path.join(directorio_raiz, anio)
    
    archivos_excel = sorted([
        f for f in os.listdir(ruta_anio)
        if f.lower().endswith((".xlsx", ".xls")) 
        and not f.startswith("~$") 
        and "DICCIONARIO" not in f.upper()
    ])
    
    print("=" * 60)
    print(f"INICIANDO CARGA DEL AÑO: {anio} | Total archivos: {len(archivos_excel)}")
    print("=" * 60)

    for i, nombre_archivo in enumerate(archivos_excel, start=1):
        ruta_completa = os.path.join(ruta_anio, nombre_archivo)
        print(f"[{i}/{len(archivos_excel)}] Procesando: {nombre_archivo}...")

        try:
            xls = pd.ExcelFile(ruta_completa)
            nombre_hoja = "CONOSCE" if "CONOSCE" in xls.sheet_names else xls.sheet_names[0]

            df = pd.read_excel(xls, sheet_name=nombre_hoja, dtype=dtype_dict)
            df.columns = [c.strip().lower() for c in df.columns]

            for col in columnas_fecha:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

            if "descripcion_orden" in df.columns:
                df["descripcion_orden"] = (
                    df["descripcion_orden"]
                    .astype(str)
                    .str.replace(r"[\r\n]+", " ", regex=True)
                    .str.strip()
                )

            filas_archivo = len(df)
            print(f"   -> Insertando {filas_archivo:,} filas...")
            
            df.to_sql(
                name="Fact_Ordenes_Compra",
                con=engine,
                if_exists="append",
                index=False,
                chunksize=10000
            )

            total_filas_insertadas += filas_archivo
            total_archivos_procesados += 1
            print(f"   -> {nombre_archivo} cargado exitosamente.")

            del df
            del xls

        except Exception as e:
            print(f"   [!] Error crítico en archivo {nombre_archivo}: {e}")

print("\n" + "=" * 60)
print("¡PROCESO DE INGESTA HISTÓRICA FINALIZADO CON ÉXITO!")
print(f"Total de archivos procesados: {total_archivos_procesados}")
print(f"Total de filas acumuladas insertadas: {total_filas_insertadas:,}")
print("=" * 60)