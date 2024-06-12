CREATE PROCEDURE UpdateUserSettings
    @UserID INT,
    @NotificationPreference BIT,
    @PrivacyLevel NVARCHAR(50),
    @Theme NVARCHAR(50),
    @Language NVARCHAR(50)

AS
BEGIN
SET NOCOUNT ON;

UPDATE Settings
SET NotificationPreference = @NotificationPreference,
 PrivacyLevel = @PrivacyLevel,
 Theme = @Theme,
 Language = @Language
WHERE UserID = @UserID;
END

select * from Settings