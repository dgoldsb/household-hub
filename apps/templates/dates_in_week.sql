SELECT
    DISTINCT date_todo
FROM
    chorelog
WHERE
    date_todo > DATE('now','weekday 0','{} days')
    AND date_todo < DATE('now','weekday 0','{} days')