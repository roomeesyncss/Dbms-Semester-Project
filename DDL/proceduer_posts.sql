--user post view

CREATE PROCEDURE GetUserPosts
    @Username NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserID INT;

    -- Fetch the user ID based on the username
    SELECT @UserID = UserID
    FROM Users
    WHERE Username = @Username;

    -- Fetch posts from the user and their mutual friends
    SELECT
        Users.Username,
        Posts.Content,
        Posts.Timestamp,
        (SELECT COUNT(*) FROM Likes WHERE Likes.PostID = Posts.PostID) AS LikeCount,
        (SELECT COUNT(*) FROM Comments WHERE Comments.PostID = Posts.PostID) AS CommentCount,
        (SELECT COUNT(*) FROM Shares WHERE Shares.PostID = Posts.PostID) AS ShareCount,
        Posts.PostID
    FROM Posts
    INNER JOIN Users ON Posts.UserID = Users.UserID
    WHERE Posts.UserID IN (
        SELECT Friendships.UserID2
        FROM Friendships
        WHERE Friendships.UserID1 = @UserID AND Friendships.Status = 'Accepted'
        UNION
        SELECT Friendships.UserID1
        FROM Friendships
        WHERE Friendships.UserID2 = @UserID AND Friendships.Status = 'Accepted'
        UNION
        SELECT @UserID
    )
    ORDER BY Posts.Timestamp DESC;
END;


CREATE PROCEDURE dbo.CreatePost
    @UserID INT,
    @Content VARCHAR(1000)
AS
BEGIN
    INSERT INTO Posts (UserID, Content, Timestamp)
    VALUES (@UserID, @Content, GETDATE());
END;





CREATE PROCEDURE ToggleLikePost
    @Username NVARCHAR(50),
    @PostID INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @UserID INT;

    -- Fetch the user ID based on the username
    SELECT @UserID = UserID
    FROM Users
    WHERE Username = @Username;

    -- Check if the user has already liked the post
    IF EXISTS (SELECT 1 FROM Likes WHERE UserID = @UserID AND PostID = @PostID)
    BEGIN
        -- Unlike the post
        DELETE FROM Likes
        WHERE UserID = @UserID AND PostID = @PostID;
    END
    ELSE
    BEGIN
        -- Like the post
        INSERT INTO Likes (UserID, PostID)
        VALUES (@UserID, @PostID);
    END

    -- Return the updated like count
    SELECT COUNT(*) AS LikeCount
    FROM Likes
    WHERE PostID = @PostID;
END;

