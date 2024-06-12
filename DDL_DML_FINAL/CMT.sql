
-- Add Comment
Alter PROCEDURE AddCommentToPost
    @PostID INT,
    @UserID INT,
    @Content VARCHAR(1000)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    INSERT INTO Comments (PostID, UserID, Content)
    VALUES (@PostID, @UserID, @Content);

    IF @@ROWCOUNT > 0
    BEGIN
        PRINT 'Comment added successfully.';

        DECLARE @AuthorID INT;
        SELECT @AuthorID = AuthorID FROM Post WHERE PostID = @PostID;

        DECLARE @CommenterUsername VARCHAR(100);
        SELECT @CommenterUsername = Username FROM [User] WHERE UserID = @UserID;

        DECLARE @NotificationContent VARCHAR(1000);
        SET @NotificationContent = @CommenterUsername + ' added a new comment to your post';

        INSERT INTO Notification (UserID, Content)
        VALUES (@AuthorID, @NotificationContent);

        IF @@ROWCOUNT > 0
            PRINT 'Notification sent to the author.';
        ELSE
            PRINT 'Failed to send notification.';
    END
    ELSE
        PRINT 'Failed to add comment.';
END;

EXEC AddCommentToPost @PostID = 1, @UserID = 2, @Content = 'This is a test comment.';

-- Get Comments Of A Post
Alter PROCEDURE GetCommentsForPost
    @PostID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    SELECT c.CommentID, c.Content, c.CreatedAt, c.UserID, u.UserName
    FROM Comments c
    INNER JOIN [User] u ON c.UserID = u.UserID
    WHERE c.PostID = @PostID;
END;


EXEC GETCOMMENTSFORPOST 6


CREATE PROCEDURE GetNotifications
    @UserID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    SELECT NotificationID, Content, CreatedAt
    FROM Notification
    WHERE UserID = @UserID
    ORDER BY CreatedAt DESC;

    PRINT 'Notifications retrieved successfully.';
END;

EXEC GetNotifications @UserID = 1