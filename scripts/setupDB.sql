CREATE TABLE persons
(
    UID INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    active BIT NOT NULL,
    email VARCHAR(50)
);
CREATE TABLE person_chore
(
    CID INT NOT NULL,
    UID INT NOT NULL
);
CREATE TABLE chores
(
    CID INT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);
CREATE TABLE chores_unplanned
(
    CID INT NOT NULL,
    UID INT,
    date_todo DATE
);
CREATE TABLE chorelog
(
    UID INT NOT NULL, 
    CID INT NOT NULL,
    finished BIT NOT NULL,
    date_todo DATE NOT NULL,
    date_finished DATE
);

