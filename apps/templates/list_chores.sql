SELECT
    DISTINCT a.CID,
    b.chore
FROM (
    SELECT
        *
    FROM chorelog
    WHERE
        date_todo > DATE('now','weekday 0','{} days')
        AND date_todo < DATE('now','weekday 0','{} days')) as a
    LEFT JOIN (
        SELECT
            name as chore,
            CID FROM chores) as b
        ON a.CID = b.CID;
