import os
import pandas as pd
from sqlalchemy import create_engine
import urllib

# Configuración del motor SQL Server con ODBC Driver 17
SERVER = 'localhost' # Modificar según el servidor
DATABASE = 'OSCE_Auditoria'

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

def cargar_archivo_chunked(ruta_archivo, chunksize=50000):
    """Carga archivos masivos por bloques asegurando tipificación estricta de RUC"""
    print(f"Iniciando carga de: {ruta_archivo}")
    for i, chunk in enumerate(pd.read_csv(ruta_archivo, chunksize=chunksize, dtype={'ruc_entidad': str, 'ruc_contratista': str})):
        chunk.rename(columns={
            'ruc_entidad': 'RUC_Entidad',
            'entidad': 'Entidad',
            'departamento_entidad': 'Departamento_Entidad',
            'nro_de_orden': 'Nro_De_Orden',
            'tipoorden': 'TipoOrden',
            'tipodecontratacion': 'TipoDeContratacion',
            'ruc_contratista': 'RUC_Contratista',
            'nombre_razon_contratista': 'Nombre_Razon_Contratista',
            'monto_total_orden_original': 'Monto_Total_Orden_Original',
            'moneda': 'Moneda',
            'fecha_de_emision': 'Fecha_De_Emision',
            'fecha_registro': 'Fecha_Registro'
        }, inplace=True)
        
        chunk['Fecha_De_Emision'] = pd.to_datetime(chunk['Fecha_De_Emision'], errors='coerce')
        chunk['Fecha_Registro'] = pd.to_datetime(chunk['Fecha_Registro'], errors='coerce')
        
        chunk.to_sql('Fact_Ordenes_Compra', con=engine, if_exists='append', index=False)
        print(f"Lote {i+1} insertado ({chunksize} registros).")

if __name__ == "__main__":
    print("Pipeline ETL listo para ejecutarse sobre data/raw/")
