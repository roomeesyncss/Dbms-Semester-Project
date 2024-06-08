ALTER TABLE Events
ADD EventCategoryID INT Unique;

ALTER TABLE Events
ADD FOREIGN KEY (EventCategoryID) REFERENCES EventCategories(EventCategoryID);


CREATE TABLE EventCategories (
    EventCategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(255) NOT NULL UNIQUE
);

ALTER TABLE Events
ADD EventCategoryID INT;

ALTER TABLE Events
ADD FOREIGN KEY (EventCategoryID) REFERENCES EventCategories(EventCategoryID);
CREATE TABLE [Events] (
    EventID INT PRIMARY KEY IDENTITY(1,1),
    EventName NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX),
    Location NVARCHAR(255),
    StartTime DATETIME NOT NULL,
    CreatedBy INT NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CreatedBy) REFERENCES [User](UserID)
);

CREATE TABLE EventSubscribers (
    EventSubscriberID INT PRIMARY KEY IDENTITY(1,1),
    EventID INT NOT NULL,
    UserID INT NOT NULL,
    SubscriptionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (UserID) REFERENCES [User](UserID)
);



--views
CREATE VIEW GetAllEvents AS
SELECT
    E.EventID,
    E.EventName,
    E.Description,
    E.Location,
    E.StartTime,
    E.CreatedBy,
    E.CreatedAt,
    EC.CategoryName,  -- Include the category name
    ISNULL(ES.SubscriberCount, 0) AS SubscriberCount
FROM Events E
LEFT JOIN (
    SELECT EventID, COUNT(*) AS SubscriberCount
    FROM EventSubscribers
    GROUP BY EventID
) ES ON E.EventID = ES.EventID
LEFT JOIN EventCategories EC ON E.EventCategoryID = EC.EventCategoryID;  -- Join with EventCategories to get the category name



CREATE VIEW GetEventSubscribers AS
SELECT
    ES.EventSubscriberID,
    ES.EventID,
    E.EventName,
    ES.UserID,
    U.Username,
    ES.SubscriptionDate
FROM EventSubscribers ES
INNER JOIN [User] U ON ES.UserID = U.UserID
INNER JOIN Events E ON ES.EventID = E.EventID;

--procedures for given functioanlity

CREATE PROCEDURE CreateEvent
    @EventName NVARCHAR(255),
    @Description NVARCHAR(MAX),
    @Location NVARCHAR(255),
    @StartTime DATETIME,
    @CreatedBy INT,
    @EventCategoryID INT  -- Include the category ID
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Events (EventName, Description, Location, StartTime, CreatedBy, EventCategoryID)
    VALUES (@EventName, @Description, @Location, @StartTime, @CreatedBy, @EventCategoryID);

    -- Return the ID of the newly created event
    SELECT SCOPE_IDENTITY() AS NewEventID;
END;


CREATE PROCEDURE SubscribeToEvent
    @EventID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM EventSubscribers
        WHERE EventID = @EventID AND UserID = @UserID
    )
    BEGIN
        PRINT 'User is already subscribed to the event';
    END
    ELSE
    BEGIN
        INSERT INTO EventSubscribers (EventID, UserID, SubscriptionDate)
        VALUES (@EventID, @UserID, GETDATE());

        PRINT 'Subscription successful';
    END
END;


CREATE PROCEDURE UnsubscribeFromEvent
    @EventID INT,
    @UserID INT
AS
BEGIN
    SET NOCOUNT ON;

    DELETE FROM EventSubscribers
    WHERE EventID = @EventID AND UserID = @UserID;

    PRINT 'Unsubscription successful';
END;




CREATE PROCEDURE UpdateEvent
    @EventID INT,
    @EventName NVARCHAR(255),
    @Description NVARCHAR(MAX),
    @Location NVARCHAR(255),
    @StartTime DATETIME,
    @EventCategoryID INT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Events
    SET EventName = @EventName,
        Description = @Description,
        Location = @Location,
        StartTime = @StartTime,
        EventCategoryID = @EventCategoryID
    WHERE EventID = @EventID;

    PRINT 'Event updated successfully';
END;






CREATE PROCEDURE DeleteEvent
    @EventID INT
AS
BEGIN
    SET NOCOUNT ON;

    -- First, delete all subscriptions related to this event to maintain referential integrity
    DELETE FROM EventSubscribers WHERE EventID = @EventID;

    -- Then, delete the event itself
    DELETE FROM Events WHERE EventID = @EventID;

    PRINT 'Event and related subscriptions deleted successfully';
END;





CREATE VIEW GetAllEvents AS
SELECT
    E.EventID,
    E.EventName,
    E.Description,
    E.Location,
    E.StartTime,
    E.CreatedBy,
    E.CreatedAt,
    EC.CategoryName,  -- Include the category name
    ISNULL(ES.SubscriberCount, 0) AS SubscriberCount
FROM Events E
LEFT JOIN (
    SELECT EventID, COUNT(*) AS SubscriberCount
    FROM EventSubscribers
    GROUP BY EventID
) ES ON E.EventID = ES.EventID
LEFT JOIN EventCategories EC ON E.EventCategoryID = EC.EventCategoryID;  -- Join with EventCategories to get the category name



CREATE VIEW GetEventSubscribers AS
SELECT
    ES.EventSubscriberID,
    ES.EventID,
    E.EventName,
    ES.UserID,
    U.Username,
    ES.SubscriptionDate
FROM EventSubscribers ES
INNER JOIN [User] U ON ES.UserID = U.UserID
INNER JOIN Events E ON ES.EventID = E.EventID;


