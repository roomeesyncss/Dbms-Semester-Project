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
CREATE TABLE Friendships (
    FriendshipID INT PRIMARY KEY IDENTITY(1,1),
    UserID1 INT NOT NULL,
    UserID2 INT NOT NULL,
    Status NVARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (Status IN ('Pending', 'Accepted', 'Rejected')),
    FOREIGN KEY (UserID1) REFERENCES [User](UserID),
    FOREIGN KEY (UserID2) REFERENCES [User](UserID)
);

CREATE TABLE Post (
    PostID INT PRIMARY KEY IDENTITY(1,1),
    AuthorID INT NOT NULL,
    Content VARCHAR(1000) NOT NULL,
    PageID INT NULL,
	CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AuthorID) REFERENCES [User](UserID),

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

CREATE TABLE Friendships (
    FriendshipID INT PRIMARY KEY IDENTITY(1,1),
    UserID1 INT NOT NULL,
    UserID2 INT NOT NULL,
    Status NVARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (Status IN ('Pending', 'Accepted', 'Rejected')),
    FOREIGN KEY (UserID1) REFERENCES [Users](UserID) ,
    FOREIGN KEY (UserID2) REFERENCES [Users](UserID)
);

CREATE TABLE Notification (
    NotificationID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    Content VARCHAR(1000) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_UserID_Notifications FOREIGN KEY (UserID) REFERENCES [User](UserID)
);

CREATE TABLE Chats (
    ChatID INT PRIMARY KEY IDENTITY(1,1),
    User1ID INT NOT NULL,
    User2ID INT NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (User1ID) REFERENCES [User](UserID) ,
    FOREIGN KEY (User2ID) REFERENCES [User](UserID)

CREATE TABLE Messages (
    MessageID INT PRIMARY KEY IDENTITY(1,1),
    ChatID INT NOT NULL,
    SenderID INT NOT NULL,
    Content VARCHAR(1000) NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ChatID) REFERENCES Chats(ChatID) ,
    FOREIGN KEY (SenderID) REFERENCES [User](UserID)
);




-- Create ReportReasons table
CREATE TABLE ReportReasons (
    ReportReasonID INT PRIMARY KEY IDENTITY(1,1),
    ReasonDescription NVARCHAR(255) NOT NULL UNIQUE
);

-- Insert dummy data into ReportReasons table
INSERT INTO ReportReasons (ReasonDescription)
VALUES
    ('Spam'),
    ('Harassment'),
    ('Inappropriate Content'),
    ('Misinformation'),
    ('Other');

CREATE TABLE Report (
    ReportID INT PRIMARY KEY IDENTITY(1,1),
    ReportedBy INT NOT NULL,
    ReportedPostID INT NOT NULL,
    ReportReasonID INT NOT NULL,
    ReportDescription NVARCHAR(MAX),
    ReportDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ReportedBy) REFERENCES [User](UserID),
    FOREIGN KEY (ReportedPostID) REFERENCES Post(PostID),
    FOREIGN KEY (ReportReasonID) REFERENCES ReportReasons(ReportReasonID)





CREATE TABLE [Events] (
    EventID INT PRIMARY KEY IDENTITY(1,1),
    EventName NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX),
    Location NVARCHAR(255),
    StartTime DATETIME NOT NULL,
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    FOREIGN KEY (EventCategoryID) REFERENCES EventCategories(EventCategoryID);
);

CREATE TABLE EventCategories (
    EventCategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(255) NOT NULL UNIQUE
);


CREATE TABLE EventSubscribers (
    EventSubscriberID INT PRIMARY KEY IDENTITY(1,1),
    EventID INT NOT NULL,
    UserID INT NOT NULL,
    SubscriptionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);



CREATE TABLE Pages (
    PageID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX),
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    IsActive BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_Pages_Users FOREIGN KEY (CreatedBy) REFERENCES [User](UserID)
);

-- Table to store roles
CREATE TABLE Roles (
    RoleID INT IDENTITY(1,1) PRIMARY KEY,
    RoleName NVARCHAR(50) NOT NULL UNIQUE
);

-- Table to store page members
CREATE TABLE PageMembers (
    PageMemberID INT IDENTITY(1,1) PRIMARY KEY,
    PageID INT NOT NULL,
    UserID INT NOT NULL,
    RoleID INT NOT NULL,
    AddedBy INT NOT NULL,
    AddedAt DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_PageMembers_Pages FOREIGN KEY (PageID) REFERENCES Pages(PageID),
    CONSTRAINT FK_PageMembers_Roles FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),
    CONSTRAINT FK_PageMembers_Users FOREIGN KEY (UserID) REFERENCES [User](UserID),
    CONSTRAINT FK_PageMembers_AddedBy FOREIGN KEY (AddedBy) REFERENCES [User](UserID)
);
CREATE TABLE Settings (
    SettingID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    NotificationPreference BIT DEFAULT 1,
    PrivacyLevel NVARCHAR(50) DEFAULT 'Public',
    Theme NVARCHAR(50) DEFAULT 'Light',
    Language NVARCHAR(50) DEFAULT 'English',
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);