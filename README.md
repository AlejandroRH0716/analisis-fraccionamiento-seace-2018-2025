# Análisis de Datos y Detección de Fraccionamiento en Contrataciones del SEACE (2018–2025)

![Estado](https://img.shields.io/badge/Estado-Completado-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SQL Server](https://img.shields.io/badge/SQL_Server-2019+-red)
![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow)

## Descripción General
Proyecto de ingeniería de datos y analítica forense enfocado en identificar patrones de riesgo, concentración contractual y presunto fraccionamiento en contrataciones menores a 8 UIT en el Estado peruano (SEACE/OSCE 2018–2025).

Se consolidaron más de **10.98 millones de transacciones válidas** que movilizaron más de **S/ 115,657 millones de soles**.

## Métricas Clave
- **Universo de Órdenes Consolidadas:** 10,986,092 transacciones oficiales.
- **Presupuesto Total Movilizado:** S/ 115,657,656,996.18.
- **Gasto en Compras Menores (<= 8 UIT):** S/ 45,424,089,970.08 (41.08% del presupuesto total y 74.27% del volumen físico de órdenes).
- **Asimetría de Montos:** Mediana nacional de S/ 2,300.00 frente a una media de S/ 10,660.21.
- **Agrupamiento al Límite (Threshold Clustering):** Más de 191,800 órdenes emitidas entre el 90% y 100% del tope anual de exoneración.

## Estructura del Repositorio
- `sql/`: Scripts DDL de base de datos, saneamiento de cadenas de texto y vistas analíticas.
- `etl/`: Pipeline en Python con procesamiento por fragmentos (chunking) y carga rápida con SQLAlchemy.
- `dashboard/`: Vistas y capturas del cuadro de mando interactivo en Power BI (3 páginas).
- `docs/`: Informe técnico y código fuente en LaTeX.

## Autor
- **Alejandro Harold Roque Huamani**
- Portafolio de Ingeniería de Datos y Analítica
