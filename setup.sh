sqlite3 hub.db < ./database/setupDB.sql
sqlite3 hub.db < ./database/initializeDB.sql
python ./scripts/updatedb.py