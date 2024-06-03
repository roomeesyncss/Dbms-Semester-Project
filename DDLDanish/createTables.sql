CREATE TABLE [User] (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    FullName NVARCHAR(100),
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NULL,
    Phone NUMERIC NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    isAdmin BIT DEFAULT 0 NOT NULL
);

CREATE TABLE Post (
    PostID INT PRIMARY KEY IDENTITY(1,1),
    AuthorID INT NOT NULL,
    Content VARCHAR(1000) NOT NULL,
    PageID INT NULL,
	CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AuthorID) REFERENCES [User](UserID),
    --FOREIGN KEY (PageID) REFERENCES Pages(PageID)
	--CONSTRAINT FK_PageID_Post FOREIGN KEY (PageID) REFERENCES Pages(PageID) ON DELETE CASCADE
);

CREATE TABLE Comments (
    CommentID INT PRIMARY KEY IDENTITY(1,1),
    PostID INT NOT NULL,
    UserID INT NOT NULL,
    Content VARCHAR(1000) NOT NULL,
	CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PostID) REFERENCES Post(PostID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);

CREATE TABLE Share (
    ShareID INT PRIMARY KEY IDENTITY(1,1),
    PostID INT NOT NULL,
    UserID INT NOT NULL,
    Shared_Platform VARCHAR(100) NULL,
    FOREIGN KEY (PostID) REFERENCES Post(PostID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);


CREATE TABLE Likes (
    LikeID INT PRIMARY KEY IDENTITY(1,1),
    PostID INT NOT NULL,
    UserID INT NOT NULL,
	CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PostID) REFERENCES Post(PostID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);

CREATE TABLE Friends (
    FriendID INT PRIMARY KEY IDENTITY(1,1),
    User1ID INT,
    User2ID INT,
    Status NVARCHAR(20) DEFAULT 'Pending' CHECK (Status IN ('Accepted', 'Rejected', 'Pending')),
    FriendAddedDate DATE,
    CONSTRAINT FK_User1ID FOREIGN KEY (User1ID) REFERENCES [User](UserID),
    CONSTRAINT FK_User2ID FOREIGN KEY (User2ID) REFERENCES [User](UserID)
);

CREATE TABLE Notifications (
    NotificationID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    Content VARCHAR(1000) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_UserID_Notifications FOREIGN KEY (UserID) REFERENCES [User](UserID)
);

CREATE TABLE Chat (
    ChatID INT PRIMARY KEY IDENTITY(1,1),
    SenderID INT FOREIGN KEY REFERENCES [User](UserID),
    ReceiverID INT FOREIGN KEY REFERENCES [User](UserID)
);

CREATE TABLE Messages (
    MessageID INT PRIMARY KEY IDENTITY(1,1),
    ChatID INT FOREIGN KEY REFERENCES Chat(ChatID),
    UserID INT FOREIGN KEY REFERENCES [User](UserID),
    Content VARCHAR(2000)
);


--Remaining
-- CREATE TABLE Pages (
--     PageID VARCHAR(50) PRIMARY KEY,
--     AdminID VARCHAR(50) FOREIGN KEY REFERENCES [User](UserID),
--     Rules VARCHAR(1000),
--     Email VARCHAR(100),
--     Bio VARCHAR(1000),
--     Country VARCHAR(100),
--     Phone NUMERIC
-- );

-- CREATE TABLE PageMembers (
--     MemberID INT PRIMARY KEY IDENTITY(1,1),
--     PageID VARCHAR(50) FOREIGN KEY REFERENCES Pages(PageID),
--     UserID VARCHAR(50) FOREIGN KEY REFERENCES [User](UserID),
--     Content VARCHAR(1000)
-- );
