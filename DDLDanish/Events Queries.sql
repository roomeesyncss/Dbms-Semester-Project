-- -------- EVENT QUERIES START -------------
-- --Create Event ----
CREATE PROCEDURE CreateEvent
    @EventName NVARCHAR(255),
    @Description NVARCHAR(MAX),
    @Location NVARCHAR(255),
    @StartTime DATETIME,
    @CreatedBy INT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Events (EventName, Description, Location, StartTime, CreatedBy)
    VALUES (@EventName, @Description, @Location, @StartTime, @CreatedBy);

    SELECT SCOPE_IDENTITY() AS NewEventID;
END;

DECLARE @StartTime DATETIME = DATEADD(DAY, 3, GETDATE());
EXEC CreateEvent @EventName = 'ABC', @Description = 'ABC Description', @Location = 'Karachi', @StartTime = @StartTime, @CreatedBy = 1

-- --Subscribe to the event ---
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

EXEC SubscribeToEvent @EventID = 1, @UserID = 2



-- --Get All Events ----
CREATE VIEW GetAllEvents AS
SELECT 
    E.EventID,
    E.EventName,
    E.Description,
    E.Location,
    E.StartTime,
    E.CreatedBy,
    E.CreatedAt,
    ISNULL(ES.SubscriberCount, 0) AS SubscriberCount
FROM Events E
LEFT JOIN (
    SELECT EventID, COUNT(*) AS SubscriberCount
    FROM EventSubscribers
    GROUP BY EventID
) ES
ON E.EventID = ES.EventID;

SELECT * FROM GetAllEvents

-- -------- EVENT QUERIES END -------------