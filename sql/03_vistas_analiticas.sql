USE OSCE_Auditoria;
GO

CREATE OR ALTER VIEW vw_Resumen_Mensual_Entidades AS
SELECT 
    YEAR(Fecha_De_Emision) AS Anio,
    MONTH(Fecha_De_Emision) AS Mes,
    Departamento_Entidad,
    Entidad,
    TipoDeContratacion,
    COUNT(Nro_De_Orden) AS Total_Ordenes,
    SUM(Monto_Total_Orden_Original) AS Monto_Total,
    AVG(Monto_Total_Orden_Original) AS Ticket_Promedio
FROM Fact_Ordenes_Compra
GROUP BY 
    YEAR(Fecha_De_Emision),
    MONTH(Fecha_De_Emision),
    Departamento_Entidad,
    Entidad,
    TipoDeContratacion;
GO

CREATE OR ALTER VIEW vw_Auditoria_Proveedores AS
SELECT 
    YEAR(Fecha_De_Emision) AS Anio,
    RUC_Entidad,
    Entidad,
    Departamento_Entidad,
    TipoDeContratacion,
    RUC_Contratista,
    Nombre_Razon_Contratista,
    COUNT(Nro_De_Orden) AS Ordenes_Por_Proveedor,
    SUM(Monto_Total_Orden_Original) AS Monto_Proveedor_Sol,
    MIN(Fecha_De_Emision) AS Primera_Orden,
    MAX(Fecha_De_Emision) AS Ultima_Orden
FROM Fact_Ordenes_Compra
GROUP BY 
    YEAR(Fecha_De_Emision),
    RUC_Entidad,
    Entidad,
    Departamento_Entidad,
    TipoDeContratacion,
    RUC_Contratista,
    Nombre_Razon_Contratista;
GO
