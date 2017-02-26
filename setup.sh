sqlite3 database/hub.db < ./scripts/setupDB.sql
sqlite3 database/hub.db < ./scripts/initializeDB.sql
python ./scripts/updatedb.py