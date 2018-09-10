UPDATE
    chorelog
SET
    finished = CASE WHEN finished = 1 THEN 0 ELSE 1 END,
    date_finished = DATE('now') WHERE date_todo = '%s' AND CID = %s
