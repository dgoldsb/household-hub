SELECT
    a.first_name,
    b.finished,
    b.date_finished
FROM (
    SELECT
        finished,
        date_finished,
        UID
    FROM
        chorelog
    WHERE
        date_todo = '%s'
        AND CID = %s) as b
    LEFT JOIN (
    SELECT
        first_name,
        UID
    FROM
        housemates) as a
    ON a.UID = B.UID;
