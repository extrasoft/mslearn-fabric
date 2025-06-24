CREATE TABLE [dbo].[DimDate] (

	[DateKey] int NOT NULL, 
	[DateAltKey] date NOT NULL, 
	[DayOfWeek] int NOT NULL, 
	[WeekDayName] varchar(10) NULL, 
	[DayOfMonth] int NOT NULL, 
	[Month] int NOT NULL, 
	[MonthName] varchar(12) NULL, 
	[Year] int NOT NULL
);


GO
ALTER TABLE [dbo].[DimDate] ADD CONSTRAINT UQ_137e751a_59ce_4af9_98ec_b57796b62ccf unique NONCLUSTERED ([DateKey]);