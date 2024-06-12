ALTER PROCEDURE UserProfileById
    @UserID INT
AS
BEGIN
    SELECT UserID, Username, Email, FullName, isAdmin, CreatedAt, Country, Phone, Password
    FROM [User]
    WHERE UserID = @UserID;
END
GO
--exceution
DECLARE @UserID INT = 1;
EXEC UserProfileById @UserID;


ALTER PROCEDURE UpdateUser
    @UserID INT,
    @Username NVARCHAR(50),
    @FullName NVARCHAR(100),
    @Email VARCHAR(100),
    @Password VARCHAR(100),
    @Country VARCHAR(100),
    @Phone NUMERIC(18, 0)  --
AS
BEGIN
    UPDATE [User]
    SET Username = @Username,
        FullName = @FullName,
        Email = @Email,
        Password = @Password,
        Country = @Country,
        Phone = @Phone
    WHERE UserID = @UserID;

    IF @@ROWCOUNT > 0
        PRINT 'User updated successfully.';
    ELSE
        PRINT 'User not found.';
END;
GO
SELECT @UserName = Username, @UserEmail = Email FROM [User] WHERE UserID = @UserID;
DECLARE @NewCountry VARCHAR(100) = 'Pakistan';

-- Declare the new country value
EXEC UpdateUser @UserID, @UserName, NULL, @UserEmail, NULL, @NewCountry, NULL;


--- FOR EDIT AND DELTE POSTS
 PROCEDURE [dbo].[DeleteUserPost]
    @PostID INT
AS
BEGIN
    DELETE FROM Post
    WHERE PostID = @PostID;
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

--
Alter PROCEDURE GetUserOnlyPosts
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Fetch posts from the user only
    SELECT
        [User].Username,
        Post.Content,
        Post.CreatedAt,
        (SELECT COUNT(*) FROM Likes WHERE Likes.PostID = Post.PostID) AS LikeCount,
        (SELECT COUNT(*) FROM Comments WHERE Comments.PostID = Post.PostID) AS CommentCount,
        (SELECT COUNT(*) FROM Share WHERE Share.PostID = Post.PostID) AS ShareCount,
        Post.PostID
    FROM Post
    INNER JOIN [User] ON Post.AuthorID = [User].UserID
    WHERE Post.AuthorID = @UserID
    ORDER BY Post.CreatedAt DESC;
END;


-- Declare variables
DECLARE @PostID INT = 1; --
DECLARE @NewContent NVARCHAR(MAX) = 'This is the new content for the post.';

-- Execute the procedure
EXEC EditUserPost @PostID, @NewContent;

DECLARE @UserID INT = 1; --

-- Execute the procedure
EXEC GetUserOnlyPosts @UserID;