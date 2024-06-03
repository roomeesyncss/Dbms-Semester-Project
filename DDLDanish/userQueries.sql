--Creating the user
INSERT INTO [User] (Username, FullName, Email, Password)
VALUES ('Rooma', 'Rooma Siddiqui', 'rooma@gmail.com', 'Abc12345%');

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

--Deleting the user
CREATE PROCEDURE DeleteUser
    @UserID VARCHAR(50)
AS
BEGIN
    IF EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        DELETE FROM [User]
        WHERE UserID = @UserID;

        PRINT 'User deleted successfully.';
    END
    ELSE
    BEGIN
        PRINT 'User not found.';
    END
END

--EXEC DeleteUser @UserID = '1'

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

    IF EXISTS (SELECT 1 FROM Friends WHERE (User1ID = @SenderID AND User2ID = @ReceiverID) OR (User1ID = @ReceiverID AND User2ID = @SenderID))
    BEGIN
        PRINT 'Error: Friendship already exists or request already sent.';
        RETURN;
    END

    INSERT INTO Friends (User1ID, User2ID, FriendAddedDate)
    VALUES (@SenderID, @ReceiverID, GETDATE());

    PRINT 'Friend request sent successfully.';
END

EXEC SendFriendRequest @SenderID = '2', @ReceiverID = '4'


-- Accept/Reject Friend Request
CREATE PROCEDURE RespondToFriendRequest
    @SenderUserID INT,
    @ReceiverUserID INT,
    @Response NVARCHAR(20)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Friends WHERE User1ID = @SenderUserID AND User2ID = @ReceiverUserID AND Status = 'Pending')
    BEGIN
        PRINT 'Error: No request pending.';
        RETURN;
    END

    IF @Response NOT IN ('Accepted', 'Rejected')
    BEGIN
        PRINT 'Error: Response must be either "Accepted" or "Rejected".';
        RETURN;
    END

    UPDATE Friends
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

EXEC RespondToFriendRequest @SenderUserID = '2', @ReceiverUserID = '4', @Response = 'Accepted'


-- Get Friends Of A User
CREATE PROCEDURE GetFriends
    @UserID INT
AS
BEGIN
    SELECT u.UserID, u.Username, u.Email, u.FullName, f.Status
    FROM Friends f
    INNER JOIN [User] u ON (f.User1ID = u.UserID OR f.User2ID = u.UserID)
    WHERE (@UserID = f.User1ID OR @UserID = f.User2ID)
        AND f.Status = 'Accepted'
        AND u.UserID != @UserID;
END;


EXEC GetFriends @UserID = 2

-- -------- FRIENDSHIP QUERIES END -------------


-- -------- NOTIFICATIONS QUERIES START -------------


-- -------- NOTIFICATIONS QUERIES START -------------