---- Table to store pages
--CREATE TABLE Pages (
--    PageID INT IDENTITY(1,1) PRIMARY KEY,
--    Title NVARCHAR(255) NOT NULL,
--    Description NVARCHAR(MAX),
--    CreatedBy INT NOT NULL,
--    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
--    UpdatedAt DATETIME NULL,
--    IsActive BIT NOT NULL DEFAULT 1,
--    CONSTRAINT FK_Pages_Users FOREIGN KEY (CreatedBy) REFERENCES [User](UserID)
--);
--
---- Table to store roles
--CREATE TABLE Roles (
--    RoleID INT IDENTITY(1,1) PRIMARY KEY,
--    RoleName NVARCHAR(50) NOT NULL UNIQUE
--);
--
--
---- Table to store page members
--CREATE TABLE PageMembers (
--    PageMemberID INT IDENTITY(1,1) PRIMARY KEY,
--    PageID INT NOT NULL,
--    UserID INT NOT NULL,
--    RoleID INT NOT NULL,
--    AddedBy INT NOT NULL,
--    AddedAt DATETIME NOT NULL DEFAULT GETDATE(),
--    CONSTRAINT FK_PageMembers_Pages FOREIGN KEY (PageID) REFERENCES Pages(PageID) ON DELETE CASCADE,
--    CONSTRAINT FK_PageMembers_Roles FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),
--    CONSTRAINT FK_PageMembers_Users FOREIGN KEY (UserID) REFERENCES [User](UserID),
--    CONSTRAINT FK_PageMembers_AddedBy FOREIGN KEY (AddedBy) REFERENCES [User](UserID)
--);
--
---- Stored procedure to create a new page
--aLTER PROCEDURE CreatePage
--    @Title NVARCHAR(255),
--    @Description NVARCHAR(MAX),
--    @CreatedBy INT
--AS
--BEGIN
--    INSERT INTO Pages (Title, Description, CreatedBy, CreatedAt, IsActive)
--    VALUES (@Title, @Description, @CreatedBy, GETDATE(), 1);
--END
--
---- Stored procedure to add a member to a page
--ALTER PROCEDURE AddPageMember
--    @PageID INT,
--    @UserID INT,
--    @RoleID INT,
--    @AddedBy INT
--AS
--BEGIN
--    INSERT INTO PageMembers (PageID, UserID, RoleID, AddedBy, AddedAt)
--    VALUES (@PageID, @UserID, @RoleID, @AddedBy, GETDATE());
--END
--
---- Stored procedure to view all active pages with their details
--ALTER PROCEDURE ViewPagesWithDetails
--AS
--BEGIN
--    SELECT
--        p.PageID,
--        p.Title AS PageName,
--        u.Username,
--        p.CreatedAt
--    FROM
--        Pages p
--    JOIN
--        [User] u ON p.CreatedBy = u.UserID
--    WHERE
--        p.IsActive = 1
--    ORDER BY
--        p.CreatedAt DESC;
--END
--
---- Stored procedure to view members of a specific page
--ALTER PROCEDURE ViewPageMembers
--    @PageID INT
--AS
--BEGIN
--    SELECT
--        pm.PageMemberID,
--        pm.UserID,
--        u.Username,
--        r.RoleName,
--        pm.AddedBy,
--        pm.AddedAt
--    FROM
--        PageMembers pm
--    JOIN
--        [User] u ON pm.UserID = u.UserID
--    JOIN
--        Roles r ON pm.RoleID = r.RoleID
--    WHERE
--        pm.PageID = @PageID;
--END
--
---- Add roles to the Roles table (Assuming roles need to be pre-populated)
--INSERT INTO Roles (RoleName) VALUES ('Admin'), ('Member');
--
---- Stored procedure to get members of a specific page by PageID
--ALTER PROCEDURE GetPageMembers
--    @PageID INT
--AS
--BEGIN
--    SELECT
--        pm.PageMemberID,
--        pm.UserID,
--        u.Username,
--        r.RoleName,
--        pm.AddedBy,
--        pm.AddedAt
--    FROM
--        PageMembers pm
--    JOIN
--        [User] u ON pm.UserID = u.UserID
--    JOIN
--        Roles r ON pm.RoleID = r.RoleID
--    WHERE
--        pm.PageID = @PageID;
--END

-- Table to store pages
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

drop table pages
-- Table to store page members
CREATE TABLE PageMembers (
    PageMemberID INT IDENTITY(1,1) PRIMARY KEY,
    PageID INT NOT NULL,
    UserID INT NOT NULL,
    RoleID INT NOT NULL,
    AddedBy INT NOT NULL,
    AddedAt DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_PageMembers_Pages FOREIGN KEY (PageID) REFERENCES Pages(PageID) ON DELETE CASCADE,
    CONSTRAINT FK_PageMembers_Roles FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),
    CONSTRAINT FK_PageMembers_Users FOREIGN KEY (UserID) REFERENCES [User](UserID),
    CONSTRAINT FK_PageMembers_AddedBy FOREIGN KEY (AddedBy) REFERENCES [User](UserID)
);


-- Pre-populating Roles table with basic roles
INSERT INTO Roles (RoleName) VALUES ('Admin'), ('Member');


-- Procedure to create a new page and assign the creator as an admin
CREATE PROCEDURE CreatePage
    @Title NVARCHAR(255),
    @Description NVARCHAR(MAX),
    @CreatedBy INT
AS
BEGIN
    BEGIN TRANSACTION;

    -- Insert the page
    INSERT INTO Pages (Title, Description, CreatedBy)
    VALUES (@Title, @Description, @CreatedBy);

    DECLARE @PageID INT;
    SET @PageID = SCOPE_IDENTITY();

    -- Assign the creator as an admin of the page
    INSERT INTO PageMembers (PageID, UserID, RoleID, AddedBy)
    VALUES (@PageID, @CreatedBy, 1, @CreatedBy);  -- RoleID 1 is Admin

    COMMIT TRANSACTION;
END;
GO

-- Procedure to view pages where the user is an admin or a creator
CREATE PROCEDURE ViewPagesWithDetails
    @UserID INT
AS
BEGIN
    SELECT p.PageID, p.Title AS PageName, u.Username AS Creator, p.CreatedAt
    FROM Pages p
    JOIN [User] u ON p.CreatedBy = u.UserID
    WHERE p.IsActive = 1 AND (
        p.CreatedBy = @UserID OR
        EXISTS (SELECT 1 FROM PageMembers pm WHERE pm.PageID = p.PageID AND pm.UserID = @UserID AND pm.RoleID = 1)
    );
END;
GO

-- Procedure to get members of a specific page
CREATE PROCEDURE GetPageMembers
    @PageID INT
AS
BEGIN
    SELECT u.Username, r.RoleName, a.Username AS AddedBy, pm.AddedAt
    FROM PageMembers pm
    JOIN [User] u ON pm.UserID = u.UserID
    JOIN Roles r ON pm.RoleID = r.RoleID
    JOIN [User] a ON pm.AddedBy = a.UserID
    WHERE pm.PageID = @PageID;
END;
GO

-- Procedure to add a member to a page (only if the current user is an admin)
CREATE PROCEDURE AddPageMember
    @PageID INT,
    @UserID INT,
    @RoleID INT,
    @AddedBy INT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM PageMembers WHERE PageID = @PageID AND UserID = @AddedBy AND RoleID = 1)
    BEGIN
        INSERT INTO PageMembers (PageID, UserID, RoleID, AddedBy)
        VALUES (@PageID, @UserID, @RoleID, @AddedBy);
    END
    ELSE
    BEGIN
        RAISERROR ('You do not have permission to add members to this page.', 16, 1);
    END
END;