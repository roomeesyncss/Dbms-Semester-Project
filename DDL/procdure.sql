--FOR MESSAGES CLass

CREATE PROCEDURE UpdateUserProf
    @Username NVARCHAR(50),
    @Email VARCHAR(100),
    @FullName NVARCHAR(100),
    @Country NVARCHAR(100),
    @Phone VARCHAR(15)
AS
BEGIN
    UPDATE Users
    SET Email = @Email, FullName = @FullName, Country = @Country, Phone = @Phone
    WHERE Username = @Username;
END

--view pfp
CREATE PROCEDURE UserProfile
    @Username NVARCHAR(50)
AS
BEGIN
    SELECT UserID, Username, Email, FullName, isAdmin, Timestamp, Country, Phone
    FROM Users
    WHERE Username = @Username;
END


--MESSAGES CLASS
CREATE PROCEDURE GetUserId
    @Username NVARCHAR(50)
AS
BEGIN
    SELECT UserID FROM Users WHERE Username = @Username;
END


--rertieve chats dear
CREATE PROCEDURE GetChats
    @UserID INT
AS
BEGIN
    SELECT c.ChatID, u1.Username AS User1, u2.Username AS User2
    FROM Chats c
    JOIN Users u1 ON c.User1ID = u1.UserID
    JOIN Users u2 ON c.User2ID = u2.UserID
    WHERE c.User1ID = @UserID OR c.User2ID = @UserID;
END


--mesages
CREATE PROCEDURE GetMessages
    @ChatID INT
AS
BEGIN
    SELECT u.Username, m.Content, m.Timestamp
    FROM Messages m
    JOIN Users u ON m.SenderID = u.UserID
    WHERE m.ChatID = @ChatID
    ORDER BY m.Timestamp DESC;
END

--newhct
CREATE PROCEDURE StartNewChat
    @User1ID INT,
    @User2ID INT
AS
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Chats
        WHERE (User1ID = @User1ID AND User2ID = @User2ID) OR (User1ID = @User2ID AND User2ID = @User1ID)
    )
    BEGIN
        INSERT INTO Chats (User1ID, User2ID)
        VALUES (@User1ID, @User2ID);
    END
END

--send msg for ebtter comm
CREATE PROCEDURE SendMessage
    @ChatID INT,
    @SenderID INT,
    @Content VARCHAR(1000)
AS
BEGIN
    INSERT INTO Messages (ChatID, SenderID, Content)
    VALUES (@ChatID, @SenderID, @Content);
END


--for deleting users onlyyyy

CREATE PROCEDURE GetAllUsers
AS
BEGIN
 SELECT UserID, Username, Email, IsAdmin
 FROM Users
END



--for admin only


CREATE PROCEDURE deleteUser
@UserID int
AS
BEGIN
DELETE FROM Users WHERE UserID = @UserID
END
