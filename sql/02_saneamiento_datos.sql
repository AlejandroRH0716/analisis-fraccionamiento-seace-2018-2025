USE OSCE_Auditoria;
GO

-- 1. Delimitación temporal estricta (2018 a 2025)
DELETE FROM Fact_Ordenes_Compra
WHERE YEAR(Fecha_De_Emision) >= 2026 
   OR YEAR(Fecha_Registro) >= 2026
   OR Fecha_De_Emision >= '2026-01-01'
   OR Fecha_Registro >= '2026-01-01'
   OR YEAR(Fecha_De_Emision) < 2018;
GO

-- 2. Homologación canónica de la causal de compras menores
UPDATE Fact_Ordenes_Compra
SET TipoDeContratacion = 'Contrataciones hasta 8 UIT'
WHERE TipoDeContratacion LIKE '%hasta 8 UIT%';
GO

-- 3. Limpieza de comillas simples, dobles y caracteres especiales en contratistas
UPDATE Fact_Ordenes_Compra
SET Nombre_Razon_Contratista = REPLACE(REPLACE(Nombre_Razon_Contratista, CHAR(34), ''), CHAR(39), '')
WHERE Nombre_Razon_Contratista LIKE '%' + CHAR(34) + '%' 
   OR Nombre_Razon_Contratista LIKE '%' + CHAR(39) + '%';

-- 4. Corrección ortográfica de la letra Ñ
UPDATE Fact_Ordenes_Compra
SET Nombre_Razon_Contratista = REPLACE(Nombre_Razon_Contratista, '¿', 'Ñ')
WHERE Nombre_Razon_Contratista LIKE '%¿%';

-- 5. Supresión de caracteres especiales iniciales residuales
UPDATE Fact_Ordenes_Compra
SET Nombre_Razon_Contratista = LTRIM(SUBSTRING(Nombre_Razon_Contratista, 2, LEN(Nombre_Razon_Contratista)))
WHERE LEFT(Nombre_Razon_Contratista, 1) IN ('&', '*', ':', '@', '-', '.');
GO
