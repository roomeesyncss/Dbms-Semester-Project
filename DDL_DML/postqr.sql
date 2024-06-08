-- -------- POST QUERIES START -------------
-- Create Post
CREATE PROCEDURE CreatePost
    @AuthorID INT,
    @Content VARCHAR(1000)
AS
BEGIN
    INSERT INTO Post (AuthorID, Content)
    VALUES (@AuthorID, @Content);

    IF @@ROWCOUNT > 0
        PRINT 'Post created successfully.';
    ELSE
        PRINT 'Failed to create post.';
END;

EXEC CreatePost @AuthorID = 3, @Content = 'This is my second post.'

----Get all posts of a user
--CREATE PROCEDURE GetUserPosts
--    @UserID INT
--AS
--BEGIN
--    SELECT
--        p.PostID,
--        p.Content,
--        p.PageID,
--        p.CreatedAt,
--        u.UserID AS AuthorID,
--        u.Username AS AuthorUsername,
--        u.FullName AS AuthorFullName
--    FROM Post p
--    INNER JOIN [User] u ON p.AuthorID = u.UserID
--    WHERE p.AuthorID = @UserID;
--END;
--
--EXEC GetUserPosts @UserID = 4
CREATE PROCEDURE GetUserPosts
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Fetch posts from the user and their mutual friends
    SELECT
        [User].Username,
        Post.Content,
        Post.CreatedAt,
        (SELECT COUNT(*) FROM Likes WHERE Likes.PostID = Post.PostID) AS LikeCount,
        (SELECT COUNT(*) FROM Comments WHERE Comments.PostID = Post.PostID) AS CommentCount,
        (SELECT COUNT(*) FROM Shares WHERE Shares.PostID = Post.PostID) AS ShareCount,
        Post.PostID
    FROM Post
    INNER JOIN [User] ON Post.AuthorID = [User].UserID
    WHERE Post.AuthorID IN (
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
    ORDER BY Post.CreatedAt DESC;
END;

-- Get all posts
CREATE VIEW GetAllPosts
AS
SELECT
    p.PostID,
    p.AuthorID,
    u.Username AS AuthorUsername,
    u.FullName AS AuthorFullName,
    p.Content,
    p.PageID,
    p.CreatedAt
FROM Post p
INNER JOIN [User] u ON p.AuthorID = u.UserID;

SELECT * FROM GetAllPosts

-- -------- POST QUERIES END -------------

-- -------- LIKE QUERIES START -------------

-- Like/Unlike post
CREATE PROCEDURE ToggleLikePost
    @PostID INT,
    @UserID INT
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

    IF EXISTS (SELECT 1 FROM Likes WHERE PostID = @PostID AND UserID = @UserID)
    BEGIN
        DELETE FROM Likes WHERE PostID = @PostID AND UserID = @UserID;
        PRINT 'Post unliked successfully.';
    END
    ELSE
    BEGIN
        INSERT INTO Likes (PostID, UserID) VALUES (@PostID, @UserID);
        PRINT 'Post liked successfully.';
    END
END;

EXEC ToggleLikePost @PostID = 3, @UserID = 3

--
--CREATE PROCEDURE ToggleLikePost
--    @UserID INT,
--    @PostID INT
--AS
--BEGIN
--    SET NOCOUNT ON;
--
--    -- Check if the user exists
--    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
--    BEGIN
--        PRINT 'Error: User does not exist.';
--        RETURN;
--    END
--
--    -- Check if the post exists
--    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
--    BEGIN
--        PRINT 'Error: Post does not exist.';
--        RETURN;
--    END
--
--    -- Check if the user has already liked the post
--    IF EXISTS (SELECT 1 FROM Likes WHERE UserID = @UserID AND PostID = @PostID)
--    BEGIN
--        -- Unlike the post
--        DELETE FROM Likes
--        WHERE UserID = @UserID AND PostID = @PostID;
--        PRINT 'Post unliked successfully.';
--    END
--    ELSE
--    BEGIN
--        -- Like the post
--        INSERT INTO Likes (UserID, PostID)
--        VALUES (@UserID, @PostID);
--        PRINT 'Post liked successfully.';
--    END
--
--    -- Return the updated like count
--    SELECT COUNT(*) AS LikeCount
--    FROM Likes
--    WHERE PostID = @PostID;
--END;


-- Get Likes Of A Post
ALTER PROCEDURE GetLikesForPost
    @PostID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    SELECT l.UserID, u.UserName
    FROM Likes l
    INNER JOIN [User] u ON l.UserID = u.UserID
    WHERE l.PostID = @PostID;

    SELECT COUNT(*) AS LikeCount
    FROM Likes
    WHERE PostID = @PostID;
END;

EXEC GetLikesForPost @PostID = 3;

-- -------- LIKE QUERIES END -------------

-- -------- COMMENT QUERIES START -------------

-- Add Comment
CREATE PROCEDURE AddCommentToPost
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
        PRINT 'Comment added successfully.';
    ELSE
        PRINT 'Failed to add comment.';
END;

EXEC AddCommentToPost @PostID = 1, @UserID = 3, @Content = 'This is a test comment.';

-- Get Comments Of A Post
CREATE PROCEDURE GetCommentsForPost
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

EXEC GetCommentsForPost @PostID = 1;

-- Delete Comment
CREATE PROCEDURE DeleteComment
    @CommentID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comments WHERE CommentID = @CommentID)
    BEGIN
        PRINT 'Error: Comment does not exist.';
        RETURN;
    END

    DELETE FROM Comments WHERE CommentID = @CommentID;

    IF @@ROWCOUNT > 0
        PRINT 'Comment deleted successfully.';
    ELSE
        PRINT 'Failed to delete comment.';
END;

EXEC DeleteComment @CommentID = 2;

-- -------- COMMENT QUERIES END -------------


ALTER PROCEDURE DeleteUserPost
    @PostID INT
AS
BEGIN
    DELETE FROM Post
    WHERE PostID = @PostID;
END;
GO


CREATE PROCEDURE DeletePost
    @PostID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    DELETE FROM Post WHERE PostID = @PostID;

    IF @@ROWCOUNT > 0
        PRINT 'Post deleted successfully.';
    ELSE
        PRINT 'Failed to delete post.';
END;




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



ALTER PROCEDURE [dbo].[EditUserPost]
    @PostID INT,
    @NewContent NVARCHAR(MAX)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        RAISERROR('Error: Post does not exist.', 16, 1);
        RETURN;
    END

    UPDATE Post SET Content = @NewContent WHERE PostID = @PostID;

    IF @@ROWCOUNT > 0
        PRINT 'Post edited successfully.';
    ELSE
        RAISERROR('Failed to edit post.', 16, 1);
END;
