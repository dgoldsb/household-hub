INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(1, 'Dylan', 'Goldsborough', 1, 'dgoldsb@live.nl');
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(2, 'Coen', 'Balkestein', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(3, 'Marvin', NULL, 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(4, 'Lars', 'van Esveld', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(5, 'Wijnand', 'Schellekens', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(6, 'Silver', 'Huber', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, email)
VALUES
(7, 'Mike', 'Dörner', 1, NULL);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 1);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 1);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 2);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 2);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 3);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 3);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 4);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 4);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 5);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 5);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(1, 6);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(2, 6);
INSERT INTO housemate_chore
(CID, UID)
VALUES
(3, 7);
INSERT INTO chores
(CID, name, description)
VALUES
(3, 'Keuken schoonmaken', '');
INSERT INTO chores
(CID, name, description)
VALUES
(2, 'Badkamers schoonmaken', '');
INSERT INTO chores
(CID, name, description)
VALUES
(1, 'Gang en trappen stofzuigen', '');
INSERT INTO reminders
(RID, name, start, recurring, rec_weeks)
VALUES
(1, 'Vuilnis buiten zetten', '2017-02-20', 1, 2);
INSERT INTO reminder_housemate
(UID, RID)
VALUES
(1, 1);
