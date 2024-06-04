-- -------- Chat QUERIES Start -------------
-- SEND MESSAGE -------
CREATE PROCEDURE SendMessage
    @SenderID INT,
    @ReceiverID INT,
    @Content VARCHAR(1000)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @SenderID)
    BEGIN
        PRINT 'Error: Sender does not exist.';
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @ReceiverID)
    BEGIN
        PRINT 'Error: Receiver does not exist.';
        RETURN;
    END

    DECLARE @ChatID INT;
    SELECT @ChatID = ChatID FROM Chat WHERE (SenderID = @SenderID AND ReceiverID = @ReceiverID) OR (SenderID = @ReceiverID AND ReceiverID = @SenderID);

    IF @ChatID IS NULL
    BEGIN
        INSERT INTO Chat (SenderID, ReceiverID)
        VALUES (@SenderID, @ReceiverID);
        SET @ChatID = SCOPE_IDENTITY();
    END

    INSERT INTO Message (ChatID, UserID, Content)
    VALUES (@ChatID, @SenderID, @Content);

    IF @@ROWCOUNT > 0
        PRINT 'Message sent successfully.';
    ELSE
        PRINT 'Failed to send message.';
END;

EXEC SendMessage @SenderID = 1, @ReceiverID = 2, @Content = 'hii'

-- Get Chat And Messages -----
ALTER PROCEDURE GetChatMessages
    @UserID INT,
    @UserToChatID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserToChatID)
    BEGIN
        PRINT 'Error: User to chat with does not exist.';
        RETURN;
    END

    DECLARE @ChatID INT;
    SELECT @ChatID = ChatID 
    FROM Chat 
    WHERE (SenderID = @UserID AND ReceiverID = @UserToChatID) 
       OR (SenderID = @UserToChatID AND ReceiverID = @UserID);

	IF @ChatID IS NULL
    BEGIN
        PRINT 'Error: No chat found between the specified users.';
        RETURN;
    END

    SELECT m.MessageID, m.ChatID, m.UserID, u.UserName, m.Content, m.createdAt
    FROM Message m
    JOIN [User] u ON m.UserID = u.UserID
    WHERE m.ChatID = @ChatID
    ORDER BY m.MessageID;

    PRINT 'Chat messages retrieved successfully.';
END;

EXEC GetChatMessages @UserID = 1, @UserToChatID = 2;

-- ---Get All Chats Of A User ----
CREATE PROCEDURE GetAllChatsOfUser
    @UserID INT
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM [User] WHERE UserID = @UserID)
    BEGIN
        PRINT 'Error: User does not exist.';
        RETURN;
    END

    SELECT DISTINCT c.ChatID, 
                    CASE 
                        WHEN c.SenderID = @UserID THEN c.ReceiverID 
                        ELSE c.SenderID 
                    END AS OtherUserID,
                    u.UserName AS OtherUserName
    FROM Chat c
    JOIN [User] u ON u.UserID = CASE 
                                    WHEN c.SenderID = @UserID THEN c.ReceiverID 
                                    ELSE c.SenderID 
                                END
    WHERE c.SenderID = @UserID OR c.ReceiverID = @UserID;
END;

EXEC GetAllChatsOfUser @UserID = 1;

-- -------- Chat QUERIES End -------------