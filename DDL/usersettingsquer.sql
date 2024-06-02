CREATE TABLE Settings (
    SettingID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    NotificationPreference BIT DEFAULT 1,
    PrivacyLevel NVARCHAR(50) DEFAULT 'Public',  --
    Theme NVARCHAR(50) DEFAULT 'Light',  --
    Language NVARCHAR(50) DEFAULT 'English',  -
    FOREIGN KEY (UserID) REFERENCES [Users](UserID) ON DELETE NO ACTION ON UPDATE NO ACTION
);




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