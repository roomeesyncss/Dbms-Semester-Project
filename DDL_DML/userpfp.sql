ALTER PROCEDURE UserProfileById
    @UserID INT
AS
BEGIN
    SELECT UserID, Username, Email, FullName, isAdmin, CreatedAt, Country, Phone, Password
    FROM [User]
    WHERE UserID = @UserID;
END
GO

ALTER PROCEDURE UpdateUser
    @UserID INT,
    @Username NVARCHAR(50),
    @FullName NVARCHAR(100),
    @Email VARCHAR(100),
    @Password VARCHAR(100),
    @Country VARCHAR(100),
    @Phone NUMERIC(18, 0)  -- Use a suitable precision and scale for phone numbers
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
GO


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
    FOREIGN KEY (ReportedPostID) REFERENCES Post(PostID), -- assuming Posts table has a PostID
    FOREIGN KEY (ReportReasonID) REFERENCES ReportReasons(ReportReasonID)
);



CREATE PROCEDURE ReportPost
    @ReportedBy INT,
    @ReportedPostID INT,
    @ReportReasonID INT,
    @ReportDescription NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Report (ReportedBy, ReportedPostID, ReportReasonID, ReportDescription, ReportDate)
    VALUES (@ReportedBy, @ReportedPostID, @ReportReasonID, @ReportDescription, GETDATE());

    PRINT 'Report submitted successfully';
END;


select * from Post

select * from reportpost



CREATE VIEW AdminViewReports AS
SELECT
    R.ReportID,
    R.ReportedBy,
    U.Username AS ReportedByUsername,
    R.ReportedPostID,
    P.Content AS ReportedPostContent,
    R.ReportReasonID,
    RR.ReasonDescription AS ReportReason,
    R.ReportDescription,
    R.ReportDate
FROM
    Report R
INNER JOIN
    [User] U ON R.ReportedBy = U.UserID
LEFT JOIN
    Post P ON R.ReportedPostID = P.PostID
INNER JOIN
    ReportReasons RR ON R.ReportReasonID = RR.ReportReasonID;

	select * from AdminViewReports