-- -------- ADMIN QUERIES START -------------
CREATE VIEW AllUsers
AS
SELECT UserID, Username, FullName, Email, Country, Phone, CreatedAt
FROM [User];

SELECT * FROM AllUsers

--Deleting the user
CREATE PROCEDURE DeleteUser
    @UserID VARCHAR(50)
AS
BEGIN
    IF EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        DELETE FROM [User]
        WHERE UserID = @UserID;

        PRINT 'User deleted successfully.';
    END
    ELSE
    BEGIN
        PRINT 'User not found.';
    END
END

-- EXEC DeleteUser @UserID = '1'

-- -------- ADMIN QUERIES END -------------