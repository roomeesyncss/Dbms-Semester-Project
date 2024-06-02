CREATE PROCEDURE GetUserNotifications
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        NotificationID,
        Content,
        CreatedAt
    FROM Notifications
    WHERE UserID = @UserID
    ORDER BY CreatedAt DESC;
END;
