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

EXEC CreatePost @AuthorID = 1, @Content = 'This is my fisrt post.'

--Get all posts of a user
CREATE PROCEDURE GetUserPosts
    @UserID INT
AS
BEGIN
    SELECT 
        p.PostID,
        p.Content,
        p.PageID,
        p.CreatedAt,
        u.UserID AS AuthorID,
        u.Username AS AuthorUsername,
        u.FullName AS AuthorFullName,
		(SELECT COUNT(*) FROM [Like] l WHERE l.PostID = p.PostID) AS LikeCount,
        (SELECT COUNT(*) FROM Comment c WHERE c.PostID = p.PostID) AS CommentCount,
        (SELECT COUNT(*) FROM Share s WHERE s.PostID = p.PostID) AS ShareCount
    FROM Post p
    INNER JOIN [User] u ON p.AuthorID = u.UserID
    WHERE p.AuthorID = @UserID;
END;

EXEC GetUserPosts @UserID = 1

-- Get all posts
ALTER VIEW GetAllPosts 
AS
SELECT 
    p.PostID,
    p.AuthorID,
    u.Username AS AuthorUsername,
    u.FullName AS AuthorFullName,
    p.Content,
    p.PageID,
    p.CreatedAt,
	(SELECT COUNT(*) FROM [Like] l WHERE l.PostID = p.PostID) AS LikeCount,
    (SELECT COUNT(*) FROM Comment c WHERE c.PostID = p.PostID) AS CommentCount,
    (SELECT COUNT(*) FROM Share s WHERE s.PostID = p.PostID) AS ShareCount
FROM Post p
INNER JOIN [User] u ON p.AuthorID = u.UserID;

--SELECT * FROM GetAllPosts

-- Delete Post ----
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

--EXEC DeletePost @PostID = 1


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

    IF EXISTS (SELECT 1 FROM [Like] WHERE PostID = @PostID AND UserID = @UserID)
    BEGIN
        DELETE FROM [Like] WHERE PostID = @PostID AND UserID = @UserID;
        PRINT 'Post unliked successfully.';
    END
    ELSE
    BEGIN
        INSERT INTO [Like] (PostID, UserID) VALUES (@PostID, @UserID);
        PRINT 'Post liked successfully.';
    END
END;

--EXEC ToggleLikePost @PostID = 1, @UserID = 2

-- Get Likes Of A Post
CREATE PROCEDURE GetLikesForPost
    @PostID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    SELECT l.UserID, u.UserName
    FROM [Like] l
    INNER JOIN [User] u ON l.UserID = u.UserID
    WHERE l.PostID = @PostID;

    SELECT COUNT(*) AS LikeCount
    FROM [Like]
    WHERE PostID = @PostID;
END;

--EXEC GetLikesForPost @PostID = 3;

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

    INSERT INTO Comment (PostID, UserID, Content)
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
    FROM Comment c
    INNER JOIN [User] u ON c.UserID = u.UserID
    WHERE c.PostID = @PostID;
END;

-- EXEC GetCommentsForPost @PostID = 1;

-- Delete Comment
CREATE PROCEDURE DeleteComment
    @CommentID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comment WHERE CommentID = @CommentID)
    BEGIN
        PRINT 'Error: Comment does not exist.';
        RETURN;
    END

    DELETE FROM Comment WHERE CommentID = @CommentID;

    IF @@ROWCOUNT > 0
        PRINT 'Comment deleted successfully.';
    ELSE
        PRINT 'Failed to delete comment.';
END;

--EXEC DeleteComment @CommentID = 2;

-- -------- COMMENT QUERIES END -------------


-- -------- SHARE QUERIES START -------------
CREATE PROCEDURE SharePost
    @UserID INT,
    @PostID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM Post WHERE PostID = @PostID)
    BEGIN
        PRINT 'Error: Post does not exist.';
        RETURN;
    END

    IF EXISTS (SELECT 1 FROM Share WHERE UserID = @UserID AND PostID = @PostID)
    BEGIN
        PRINT 'Error: Post already shared by the user.';
        RETURN;
    END

    INSERT INTO Share (UserID, PostID, CreatedAt)
    VALUES (@UserID, @PostID, GETDATE());

    PRINT 'Post shared successfully.';
END;

EXEC SharePost @UserID = 1, @PostID = 1

-- -------- SHARE QUERIES END -------------