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
(3, 'Beau', 'Schaepman', 1, NULL);
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
INSERT INTO teams
(UID, TID)
VALUES
(1, 1);
INSERT INTO teams
(UID, TID)
VALUES
(2, 1);
INSERT INTO teams
(UID, TID)
VALUES
(3, 2);
INSERT INTO teams
(UID, TID)
VALUES
(6, 2);
INSERT INTO teams
(UID, TID)
VALUES
(4, 3);
INSERT INTO teams
(UID, TID)
VALUES
(7, 3);
INSERT INTO teams
(UID, TID)
VALUES
(5, 4);
INSERT INTO chores
(CID, name, description)
VALUES
(1, 'Keuken schoonmaken', '');
INSERT INTO chores
(CID, name, description)
VALUES
(2, 'Badkamer schoonmaken', '');
INSERT INTO chores
(CID, name, description)
VALUES
(3, 'Gang en trappen stofzuigen', '');
INSERT INTO chores
(CID, name, description)
VALUES
(4, 'Toilet beneden schoonmaken', '');
INSERT INTO reminders
(RID, name, start, recurring, rec_weeks)
VALUES
(1, 'Vuilnis buiten zetten', '2017-02-20', 1, 2);
INSERT INTO reminder_housemate
(UID, RID)
VALUES
(1, 1);
