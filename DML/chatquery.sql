Alter PROCEDURE GetChats
    @UserID INT
AS
BEGIN
    SELECT c.ChatID, u1.Username AS User1, u2.Username AS User2
    FROM Chats c
    JOIN [User] u1 ON c.User1ID = u1.UserID
    JOIN [User] u2 ON c.User2ID = u2.UserID
    WHERE c.User1ID = @UserID OR c.User2ID = @UserID;
END


--mesages
Alter PROCEDURE GetMessages
    @ChatID INT
AS
BEGIN
    SELECT u.Username, m.Content, m.Timestamp
    FROM Messages m
    JOIN [User] u ON m.SenderID = u.UserID
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
