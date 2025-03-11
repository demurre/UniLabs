/*  
Get a list of all businesses.
*/  
SELECT * FROM Підприємтство;
/*  
Get a list of companies with the letter “a” in their name. Sort by year of establishment.  
*/  
SELECT * FROM Підприємтство WHERE Назва LIKE '%a%' ORDER BY [Рік початку];
/*  
Get a list of businesses established in the last ten years.
*/  
SELECT * FROM Підприємтство WHERE [Рік початку] >= YEAR(GETDATE()) - 10;
/*  
Get a list of all enterprises of several forms of ownership.
*/  
SELECT Підприємтство.* 
FROM Підприємтство 
INNER JOIN [Форма власності] ON Підприємтство.[Код форми власності] = [Форма власності].[Код форми власності]
WHERE [Форма власності].[Назва форми власності] IN ("Державний", "Приватний")
/*  
Determine the amount of assistance provided to all public gardens.
*/  
SELECT SUM(CAST(Вартість AS DECIMAL))
FROM [Надання допомоги дитсадку] 
WHERE [Номер дитсадка] IN (
    SELECT [Номер дитсадка]
    FROM [Дитячий садок] 
    WHERE [Код форми власності] = 1
);
/*  
Obtain a list of companies that provided assistance to children in 2021 (specify the type of assistance).
*/  
SELECT CONVERT (DATETIME, [Надання допомоги дитині].[Дата надання], 105) AЅ [Дата надання], Підприємство.Назва,
[Вид допомоги].Вид
FROM [Надання допомоги дитині]
INNER JOIN Підприємство ON [Надання допомоги дитині].[Код підприємства] = Підприємство.[Код підприємства] 
INNER JOIN [Вид допомоги] ON [Надання допомоги дитині].[Код виду допомоги] = [Вид допомоги].[Код виду допомоги]
WHERE YEAR (CONVERT(DATETIME, [Надання допомоги дитині].[Дата надання], 105)) = 2021;
/*  
Obtain a list of companies that have provided assistance to kindergartens above the average assistance. 
*/  
SELECT Підприємство.Назва
FROM [Надання допомоги дитсадку]
INNER JOIN Підприємство ON [Надання допомоги дитсадку].[Код підприємства] = Підприємство.[Код підприємства]
WHERE САЅТ([Надання допомоги дитсадку].Вартість AS FLOAT) > 
(SELECT AVG(CAST(Вартість AS FLOAT)) FROM [Надання допомоги дитсадку]);
