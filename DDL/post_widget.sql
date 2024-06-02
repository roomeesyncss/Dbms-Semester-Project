CREATE PROCEDURE SharePost
    @PostID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Shares (PostID, UserID)
    VALUES (@PostID, @UserID);

    SELECT
        COUNT(*) AS ShareCount
    FROM Shares
    WHERE PostID = @PostID;
END;


CREATE PROCEDURE SharePost2
    @PostID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Shares (PostID, UserID)
    VALUES (@PostID, @UserID);

    DECLARE @OwnerUserID INT
    DECLARE @Content NVARCHAR(1000)

    SELECT @OwnerUserID = UserID FROM Posts WHERE PostID = @PostID

    IF @OwnerUserID IS NOT NULL AND @OwnerUserID <> @UserID
    BEGIN
        SET @Content = CONCAT('Your post with PostID ', @PostID, ' has been shared by user ', @UserID, '.')
        INSERT INTO Notifications (UserID, Content)
        VALUES (@OwnerUserID, @Content)
    END

    SET @Content = CONCAT('You have shared the post with PostID ', @PostID, '.')
    INSERT INTO Notifications (UserID, Content)
    VALUES (@UserID, @Content)

    SELECT COUNT(*) AS ShareCount
    FROM Shares
    WHERE PostID = @PostID;
END;
