ALTER PROCEDURE UserProfileById
    @UserID INT
AS
BEGIN
    SELECT UserID, Username, Email, FullName, isAdmin, CreatedAt, Country, Phone, Password
    FROM [User]
    WHERE UserID = @UserID;
END
GO

ALTER PROCEDURE UpdateUser
    @UserID INT,
    @Username NVARCHAR(50),
    @FullName NVARCHAR(100),
    @Email VARCHAR(100),
    @Password VARCHAR(100),
    @Country VARCHAR(100),
    @Phone NUMERIC(18, 0)  -- Use a suitable precision and scale for phone numbers
AS
BEGIN
    UPDATE [User]
    SET Username = @Username,
        FullName = @FullName,
        Email = @Email,
        Password = @Password,
        Country = @Country,
        Phone = @Phone
    WHERE UserID = @UserID;

    IF @@ROWCOUNT > 0
        PRINT 'User updated successfully.';
    ELSE
        PRINT 'User not found.';
END;
GO