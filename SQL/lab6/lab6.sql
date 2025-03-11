/*  
Checking the child's date of birth
*/  
CREATE TRIGGER check_birthdate
ОN Дитина
AFTER INSERT
AS
BEGIN
    IF EXISTS (SELECT * FROM inserted WHERE [Дата народження] < '2017-12-12') 
    BEGIN
        RAISERROR ('Дата народження дитини не може бути раніше 12.12.2017', 16, 1); 
        ROLLBACK TRANSACTION;
    END;
END;
/*  
Using a trigger to implement restrictions on entering values
*/
CREATE TRIGGER check_name 
ОN Дитина
AFTER INSERT
AS
BEGIN
DECLARE @ПІБ varchar(50)
SELECT @ПІБ= ПІБ
FROM inserted
IF len(@ПІБ)>51
BEGIN
ROLLBACK TRANSACTION
END
END