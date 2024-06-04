--Creating the user
INSERT INTO [User] (Username, FullName, Email, Password)
VALUES ('Rooma', 'Rooma Siddiqui', 'rooma@gmail.com', 'Abc12345%');

-- SELECT * FROM [User]

--Updating the user
CREATE PROCEDURE UpdateUser
    @UserID INT,
    @Username NVARCHAR(50),
    @FullName NVARCHAR(100),
    @Email VARCHAR(100),
    @Password VARCHAR(100),
    @Country VARCHAR(100),
    @Phone NUMERIC
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

--EXEC UpdateUser @UserID = '4', @Username = 'rooma', @FullName = 'Rooma Siddiqui', @Email = 'roomasiddiqui2003', @Password = 'Abc12345%', @Country = 'Pakistan', @Phone = '0023424234'


-- -------- FRIENDSHIP QUERIES START -------------
--Send Request
CREATE PROCEDURE SendFriendRequest
    @SenderID INT,
    @ReceiverID INT
AS
BEGIN
    IF @SenderID = @ReceiverID
    BEGIN
        PRINT 'Error: Sender and receiver cannot be the same user.';
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID IN (@SenderID, @ReceiverID))
    BEGIN
        PRINT 'Error: One or both users do not exist.';
        RETURN;
    END

    IF EXISTS (SELECT 1 FROM Friend WHERE (User1ID = @SenderID AND User2ID = @ReceiverID) OR (User1ID = @ReceiverID AND User2ID = @SenderID))
    BEGIN
        PRINT 'Error: Friendship already exists or request already sent.';
        RETURN;
    END

    INSERT INTO Friend (User1ID, User2ID, FriendAddedDate)
    VALUES (@SenderID, @ReceiverID, GETDATE());

    PRINT 'Friend request sent successfully.';
END

--EXEC SendFriendRequest @SenderID = 1, @ReceiverID = 2


-- Accept/Reject Friend Request
CREATE PROCEDURE RespondToFriendRequest
    @SenderUserID INT,
    @ReceiverUserID INT,
    @Response NVARCHAR(20)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Friend WHERE User1ID = @SenderUserID AND User2ID = @ReceiverUserID AND Status = 'Pending')
    BEGIN
        PRINT 'Error: No request pending.';
        RETURN;
    END

    IF @Response NOT IN ('Accepted', 'Rejected')
    BEGIN
        PRINT 'Error: Response must be either "Accepted" or "Rejected".';
        RETURN;
    END

    UPDATE Friend
    SET Status = @Response
    WHERE User1ID = @SenderUserID AND User2ID = @ReceiverUserID AND Status = 'Pending';

    IF @@ROWCOUNT = 1
    BEGIN
        PRINT 'Friend request ' + @Response + ' successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Error: Unable to update the friend request status.';
    END
END

--EXEC RespondToFriendRequest @SenderUserID = 1, @ReceiverUserID = 2, @Response = 'Accepted'


-- Get Friends Of A User
CREATE PROCEDURE GetFriends
    @UserID INT
AS
BEGIN
    SELECT u.UserID, u.Username, u.Email, u.FullName, f.Status
    FROM Friend f
    INNER JOIN [User] u ON (f.User1ID = u.UserID OR f.User2ID = u.UserID)
    WHERE (@UserID = f.User1ID OR @UserID = f.User2ID)
        AND f.Status = 'Accepted'
        AND u.UserID != @UserID;
END;

--EXEC GetFriends @UserID = 1

-- Get Pending Requests
CREATE PROCEDURE GetPendingFriendRequests
    @UserID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    SELECT f.User1ID AS SenderID, u.Username AS SenderUsername, u.FullName AS SenderFullName
    FROM Friend f
    INNER JOIN [User] u ON f.User1ID = u.UserID
    WHERE f.User2ID = @UserID AND f.Status = 'Pending';
    
    PRINT 'Pending friend requests retrieved successfully.';
END;

--EXEC GetPendingFriendRequests @UserID = 2;

-- -------- FRIENDSHIP QUERIES END -------------


-- -------- NOTIFICATIONS QUERIES START -------------
-- Get Notifications
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

-- -------- NOTIFICATIONS QUERIES END -------------