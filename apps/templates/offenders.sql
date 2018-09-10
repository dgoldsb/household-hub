SELECT
    a.first_name,
    IFNULL(b.chore_count,0) as chore_count
FROM (
    SELECT
        first_name,
        UID FROM persons
     ) as a
LEFT JOIN (
    SELECT
        UID,
        COUNT(*) as chore_count
    FROM
        chorelog
    WHERE
        date_todo < DATE('now','weekday 0','-6 day')  -- +1 - 7 days, to give people one week to do a chore
        AND finished = 0
    GROUP BY UID) as b
        ON a.UID = b.UID
WHERE a.first_name <> 'None'
ORDER BY chore_count DESC