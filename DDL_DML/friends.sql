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

    IF EXISTS (SELECT 1 FROM Friendships WHERE (UserID1 = @SenderID AND UserID2 = @ReceiverID) OR (UserID1 = @ReceiverID AND UserID2 = @SenderID))
    BEGIN
        PRINT 'Error: Friendship already exists or request already sent.';
        RETURN;
    END

    INSERT INTO Friendships (UserID1, UserID2, Status)
    VALUES (@SenderID, @ReceiverID, 'Pending');

    PRINT 'Friend request sent successfully.';
END



CREATE PROCEDURE RespondToFriendRequest
    @SenderUserID INT,
    @ReceiverUserID INT,
    @Response NVARCHAR(20)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Friendships WHERE UserID1 = @SenderUserID AND UserID2 = @ReceiverUserID AND Status = 'Pending')
    BEGIN
        PRINT 'Error: No request pending.';
        RETURN;
    END

    IF @Response NOT IN ('Accepted', 'Rejected')
    BEGIN
        PRINT 'Error: Response must be either "Accepted" or "Rejected".';
        RETURN;
    END

    UPDATE Friendships
    SET Status = @Response
    WHERE UserID1 = @SenderUserID AND UserID2 = @ReceiverUserID AND Status = 'Pending';

    IF @@ROWCOUNT = 1
    BEGIN
        PRINT 'Friend request ' + @Response + ' successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Error: Unable to update the friend request status.';
    END
END


CREATE PROCEDURE GetFriends
    @UserID INT
AS
BEGIN
    SELECT u.UserID, u.Username, u.Email, u.FullName, f.Status
    FROM Friendships f
    INNER JOIN [User] u ON (f.UserID1 = u.UserID OR f.UserID2 = u.UserID)
    WHERE (@UserID = f.UserID1 OR @UserID = f.UserID2)
        AND f.Status = 'Accepted'
        AND u.UserID != @UserID;
END



CREATE PROCEDURE GetPendingFriendRequests
    @UserID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    SELECT f.UserID1 AS SenderID, u.Username AS SenderUsername, u.FullName AS SenderFullName
    FROM Friendships f
    INNER JOIN [User] u ON f.UserID1 = u.UserID
    WHERE f.UserID2 = @UserID AND f.Status = 'Pending';

    PRINT 'Pending friend requests retrieved successfully.';
END
