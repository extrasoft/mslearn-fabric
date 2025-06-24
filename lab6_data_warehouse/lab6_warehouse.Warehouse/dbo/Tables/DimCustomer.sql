CREATE TABLE [dbo].[DimCustomer] (

	[CustomerKey] int NOT NULL, 
	[CustomerAltKey] varchar(50) NULL, 
	[Title] varchar(5) NULL, 
	[FirstName] varchar(50) NOT NULL, 
	[LastName] varchar(50) NULL, 
	[AddressLine1] varchar(200) NULL, 
	[City] varchar(50) NULL, 
	[StateProvince] varchar(50) NULL, 
	[CountryRegion] varchar(50) NULL, 
	[PostalCode] varchar(20) NULL
);


GO
ALTER TABLE [dbo].[DimCustomer] ADD CONSTRAINT UQ_d980bb50_405c_4f73_baed_bf30e406a8c4 unique NONCLUSTERED ([CustomerKey]);