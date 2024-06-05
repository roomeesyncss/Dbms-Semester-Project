CREATE PROCEDURE SharePost2
    @PostID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert into Share table
    INSERT INTO Share (PostID, UserID)
    VALUES (@PostID, @UserID);

    DECLARE @OwnerUserID INT;
    DECLARE @Content NVARCHAR(1000);

    -- Get the owner of the post
    SELECT @OwnerUserID = UserID FROM Post WHERE PostID = @PostID;

    -- Check if the owner exists and is not the same as the sharing user
    IF @OwnerUserID IS NOT NULL AND @OwnerUserID <> @UserID
    BEGIN
        -- Notification for the owner
        SET @Content = CONCAT('Your post with PostID ', @PostID, ' has been shared by user ', @UserID, '.');
        INSERT INTO Notification (UserID, Content)
        VALUES (@OwnerUserID, @Content);
    END;

    -- Notification for the sharing user
    SET @Content = CONCAT('You have shared the post with PostID ', @PostID, '.');
    INSERT INTO Notification (UserID, Content)
    VALUES (@UserID, @Content);

    -- Return the share count
    SELECT COUNT(*) AS ShareCount
    FROM Share
    WHERE PostID = @PostID;
END;


CREATE PROCEDURE SharePost212
    @PostID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert into Share table
    INSERT INTO Share (PostID, UserID)
    VALUES (@PostID, @UserID);

    DECLARE @OwnerUserID INT;
    DECLARE @Content NVARCHAR(1000);
    DECLARE @SharerUsername NVARCHAR(50);
    DECLARE @OwnerUsername NVARCHAR(50);

    -- Get the owner of the post and the sharer's username
    SELECT
        @OwnerUserID = AuthorID,
        @SharerUsername = Username
    FROM
        Post
    JOIN
        [User] ON [User].UserID = @UserID
    WHERE
        PostID = @PostID;

    -- Get the owner's username
    SELECT
        @OwnerUsername = Username
    FROM
        [User]
    WHERE
        UserID = @OwnerUserID;

    -- Check if the owner exists and is not the same as the sharing user
    IF @OwnerUserID IS NOT NULL AND @OwnerUserID <> @UserID
    BEGIN
        -- Notification for the owner
        SET @Content = CONCAT(@OwnerUsername, ', your post with PostID ', @PostID, ' has been shared by ', @SharerUsername, '.');
        INSERT INTO Notification (UserID, Content)
        VALUES (@OwnerUserID, @Content);
    END;

    -- Notification for the sharing user
    SET @Content = CONCAT(@SharerUsername, ', you have shared the post with PostID ', @PostID, '.');
    INSERT INTO Notification (UserID, Content)
    VALUES (@UserID, @Content);

    -- Return the share count
    SELECT COUNT(*) AS ShareCount
    FROM Share
    WHERE PostID = @PostID;
END;
