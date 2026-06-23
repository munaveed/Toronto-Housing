CREATE DATABASE TorontoHousing;
GO

USE TorontoHousing;
GO

CREATE TABLE BuildingEvaluations (
    RecordID INT PRIMARY KEY,
    SiteAddress VARCHAR(255),
    SafetyScore FLOAT,
    Neighbourhood VARCHAR(150),
    Ward VARCHAR(100)
);