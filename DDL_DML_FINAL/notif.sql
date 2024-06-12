ALTER PROCEDURE [dbo].[GetUserNotifications]
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        NotificationID,
        Content,
        CreatedAt
    FROM Notification
    WHERE UserID = @UserID
    ORDER BY CreatedAt DESC;
END;
