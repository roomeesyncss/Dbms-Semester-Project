------ -------- Chat QUERIES END -------------
------ SEND MESSAGE -------
----CREATE PROCEDURE SendMessage
----    @SenderID INT,
----    @ReceiverID INT,
----    @Content VARCHAR(1000)
----AS
----BEGIN
----    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @SenderID)
----    BEGIN
----        PRINT 'Error: Sender does not exist.';
----        RETURN;
----    END
----
----    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @ReceiverID)
----    BEGIN
----        PRINT 'Error: Receiver does not exist.';
----        RETURN;
----    END
----
----    -- Check if a chat between sender and receiver already exists
----    DECLARE @ChatID INT;
----    SELECT @ChatID = ChatID FROM Chat WHERE (SenderID = @SenderID AND ReceiverID = @ReceiverID) OR (SenderID = @ReceiverID AND ReceiverID = @SenderID);
----
----    -- If chat does not exist, create a new chat
----    IF @ChatID IS NULL
----    BEGIN
----        INSERT INTO Chat (SenderID, ReceiverID)
----        VALUES (@SenderID, @ReceiverID);
----        SET @ChatID = SCOPE_IDENTITY();
----    END
----
----    -- Insert the message into Messages table with the respective ChatID
----    INSERT INTO Messages (ChatID, UserID, Content)
----    VALUES (@ChatID, @SenderID, @Content);
----
----    IF @@ROWCOUNT > 0
----        PRINT 'Message sent successfully.';
----    ELSE
----        PRINT 'Failed to send message.';
----END;
----
----
----EXEC SendMessage @SenderID = 4, @ReceiverID = 3, @Content = 'hii'
----
------ Get Chat And Messages -----
----ALTER PROCEDURE GetChatMessages
----    @UserID INT,
----    @UserToChatID INT
----AS
----BEGIN
----    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
----    BEGIN
----        PRINT 'Error: User does not exist.';
----        RETURN;
----    END
----
----    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserToChatID)
----    BEGIN
----        PRINT 'Error: User to chat with does not exist.';
----        RETURN;
----    END
----
----    DECLARE @ChatID INT;
----    SELECT @ChatID = ChatID
----    FROM Chat
----    WHERE (SenderID = @UserID AND ReceiverID = @UserToChatID)
----       OR (SenderID = @UserToChatID AND ReceiverID = @UserID);
----
----	IF @ChatID IS NULL
----    BEGIN
----        PRINT 'Error: No chat found between the specified users.';
----        RETURN;
----    END
----
----    SELECT m.MessageID, m.ChatID, m.UserID, u.UserName, m.Content
----    FROM Messages m
----    JOIN [User] u ON m.UserID = u.UserID
----    WHERE m.ChatID = @ChatID
----    ORDER BY m.MessageID;
----
----    PRINT 'Chat messages retrieved successfully.';
----END;
----
----EXEC GetChatMessages @UserID = 3, @UserToChatID = 4;
--
--
--
--
--CREATE PROCEDURE GetChats
--    @UserID INT
--AS
--BEGIN
--    SELECT c.ChatID, u1.Username AS User1, u2.Username AS User2
--    FROM Chats c
--    JOIN Users u1 ON c.User1ID = u1.UserID
--    JOIN Users u2 ON c.User2ID = u2.UserID
--    WHERE c.User1ID = @UserID OR c.User2ID = @UserID;
--END
--
--
----mesages
--CREATE PROCEDURE GetMessages
--    @ChatID INT
--AS
--BEGIN
--    SELECT u.Username, m.Content, m.Timestamp
--    FROM Messages m
--    JOIN Users u ON m.SenderID = u.UserID
--    WHERE m.ChatID = @ChatID
--    ORDER BY m.Timestamp DESC;
--END
--
----newhct
--CREATE PROCEDURE StartNewChat
--    @User1ID INT,
--    @User2ID INT
--AS
--BEGIN
--    IF NOT EXISTS (
--        SELECT 1 FROM Chats
--        WHERE (User1ID = @User1ID AND User2ID = @User2ID) OR (User1ID = @User2ID AND User2ID = @User1ID)
--    )
--    BEGIN
--        INSERT INTO Chats (User1ID, User2ID)
--        VALUES (@User1ID, @User2ID);
--    END
--END
--
----send msg for ebtter comm
--CREATE PROCEDURE SendMessage
--    @ChatID INT,
--    @SenderID INT,
--    @Content VARCHAR(1000)
--AS
--BEGIN
--    INSERT INTO Messages (ChatID, SenderID, Content)
--    VALUES (@ChatID, @SenderID, @Content);
--END


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
