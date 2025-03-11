/*  
Write a stored procedure to get a list of all enterprises of a given form of ownership. 
*/  
CREATE PROCEDURE GetCompaniesByOwnershipForm
    @OwnershipFormCode INT
AS
BEGIN
    SELECT Підприємство.Назва AЅ [Назва_Підприемства]
    FROM Підприємство
    INNER JOIN [Форма власності] ON Підприємство.[Код форми власності] = [Форма власності].[Код форми власності] 
    WHERE [Форма власності].[Код форми власності] = @OwnershipFormCode;
END;
/*  
Write a stored procedure to get a list of all companies with the specified letter in the name.
*/ 
CREATE PROCEDURE GetCompaniesByLetterInName
    @Letter CHAR(1)
AS 
BEGIN
    SELECT *
    FROM Підприємство
    WHERE Пiдприємство.Hазва LIKE '%' + @Letter + '%';
END;
/*  
Write a stored procedure to get a list of enterprises created in the last specified years (use the GetDate() function).
*/ 
CREATE PROCEDURE GetCompaniesByCreationYear 
@YearsAgo INT
AS 
BEGIN
    DECLARE @StartDate DATE;
    SET @StartDate = DATEADD(YEAR, -@YearsAgo, GETDATE());
    
    SELECT *
    FROM Підприємство
    WHERE Підприємство.[Рік початку] >= @StartDate;
END;
/*  
Write a stored procedure to determine the amount of assistance provided to all kindergartens of a given form of ownership. 
*/ 
CREATE PROCEDURE CalculateAssistanceForOwnershipType (@OwnershipType NVARCHAR(100))
AS
BEGIN
    SELECT SUM(CONVERT (DECIMAL(18, 2), [Надання допомоги дитсадку].Вартість))
    FROM [Надання допомоги дитсадку]
    INNER JOIN [Дитячий садок] ON [Надання допомоги дитсадку].[Номер дитсадка] = [Дитячий садок].[Номер дитсадка] 
    INNER JOIN [Форма власності] ON [Дитячий садок].[Код форми власності] = [Форма власності].[Код форми власності]
    WHERE [Форма власності].[Назва форми власності] = @OwnershipType;
END;