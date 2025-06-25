 CREATE VIEW SalesLT.vw_SalesOrderHoliday AS
 SELECT DISTINCT soh.SalesOrderID, soh.OrderDate, ph.HolidayName, ph.CountryOrRegion
 FROM SalesLT.SalesOrderHeader AS soh
 INNER JOIN SalesLT.Address a
     ON a.AddressID = soh.ShipToAddressID
 INNER JOIN SalesLT.PublicHolidays AS ph
     ON soh.OrderDate = ph.Date AND a.CountryRegion = ph.CountryOrRegion
 WHERE a.CountryRegion = 'United Kingdom';

GO

