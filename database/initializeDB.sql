INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(1, 'Dylan', 'Goldsborough', 1, '620033224');
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(2, 'Coen', 'Balkestein', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(3, 'Beau', 'Schaepman', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(4, 'Lars', 'van Esveld', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(5, 'Wijnand', 'Schellekens', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(6, 'Silver', 'Huber', 1, NULL);
INSERT INTO housemates
(UID, first_name, last_name, active, phone)
VALUES
(7, 'Mike', 'Dörner', 1, NULL);
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