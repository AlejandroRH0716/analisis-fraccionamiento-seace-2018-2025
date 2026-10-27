CREATE DATABASE OSCE_Auditoria;
GO

USE OSCE_Auditoria;
GO

CREATE TABLE Fact_Ordenes_Compra (
    RUC_Entidad VARCHAR(11) NOT NULL,
    Entidad VARCHAR(250) NOT NULL,
    Departamento_Entidad VARCHAR(100) NULL,
    Nro_De_Orden VARCHAR(50) NOT NULL,
    TipoOrden VARCHAR(50) NULL,
    TipoDeContratacion VARCHAR(150) NOT NULL,
    RUC_Contratista VARCHAR(11) NOT NULL,
    Nombre_Razon_Contratista VARCHAR(250) NOT NULL,
    Monto_Total_Orden_Original DECIMAL(18, 2) NOT NULL,
    Moneda VARCHAR(20) NOT NULL,
    Fecha_De_Emision DATE NOT NULL,
    Fecha_Registro DATE NULL,
    Anio AS YEAR(Fecha_De_Emision) PERSISTED
);
GO

CREATE NONCLUSTERED INDEX IX_Fact_Contratista_Monto
ON Fact_Ordenes_Compra (RUC_Contratista, Monto_Total_Orden_Original)
INCLUDE (Nombre_Razon_Contratista, Entidad, Fecha_De_Emision);

CREATE NONCLUSTERED INDEX IX_Fact_Entidad_Tipo
ON Fact_Ordenes_Compra (RUC_Entidad, TipoDeContratacion)
INCLUDE (Monto_Total_Orden_Original, Fecha_De_Emision, Departamento_Entidad);
GO
