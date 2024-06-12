CREATE PROCEDURE GetFriends
    @UserID INT
AS
BEGIN
    SELECT [User].Username
    FROM Friendships
    INNER JOIN [User] ON Friendships.UserID2 = [User].UserID
    WHERE Friendships.UserID1 = @UserID AND Friendships.Status = 'Accepted'

    UNION

    SELECT [User].Username
    FROM Friendships
    INNER JOIN [User] ON Friendships.UserID1 = [User].UserID
    WHERE Friendships.UserID2 = @UserID AND Friendships.Status = 'Accepted'
END


CREATE PROCEDURE GetPendingFriendRequests
    @UserID INT
AS
BEGIN
    SELECT [User].Username, Friendships.FriendshipID
    FROM Friendships
    INNER JOIN [User] ON Friendships.UserID1 = [User].UserID
    WHERE Friendships.UserID2 = @UserID AND Friendships.Status = 'Pending'
END


CREATE PROCEDURE RemoveFriend
    @UserID1 INT,
    @UserID2 INT
AS
BEGIN
    DELETE FROM Friendships
    WHERE (UserID1 = @UserID1 AND UserID2 = @UserID2)
       OR (UserID1 = @UserID2 AND UserID2 = @UserID1)
END


CREATE PROCEDURE UpdateFriendRequestStatus
    @FriendshipID INT,
    @Status NVARCHAR(50)
AS
BEGIN
    UPDATE Friendships
    SET Status = @Status
    WHERE FriendshipID = @FriendshipID
END



CREATE PROCEDURE SendFriendRequest
    @UserID INT,
    @FriendID INT
AS
BEGIN
    -- Check if there's already a friendship or pending request
    IF EXISTS (SELECT 1 FROM Friendships WHERE (UserID1 = @UserID AND UserID2 = @FriendID) OR (UserID1 = @FriendID AND UserID2 = @UserID))
    BEGIN
        PRINT 'Friendship or pending request already exists.'
    END
    ELSE
    BEGIN
        -- Insert the new friend request
        INSERT INTO Friendships (UserID1, UserID2, Status)
        VALUES (@UserID, @FriendID, 'Pending')
    END
END



ALter PROCEDURE GetPotentialFriends
    @CurrentUserID INT,
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SELECT
        U.UserID,
        U.Username
    FROM
        [User] U
    WHERE
        U.UserID NOT IN (
            SELECT
                CASE
                    WHEN F.UserID1 = @CurrentUserID THEN F.UserID2
                    ELSE F.UserID1
                END
            FROM
                Friendships F
            WHERE
                (F.UserID1 = @CurrentUserID OR F.UserID2 = @CurrentUserID)
        )
    AND
        U.UserID <> @CurrentUserID
    AND
        U.Username LIKE '%' + @SearchTerm + '%'
END


EXEC GetFriends @UserID = 1;
EXEC GetPendingFriendRequests @UserID = 1;
EXEC RemoveFriend @UserID1 = 1, @UserID2 = 3;
EXEC UpdateFriendRequestStatus @FriendshipID = 5, @Status = 'Accepted';
EXEC GetPotentialFriends @CurrentUserID = 1, @SearchTerm = 'Da';
