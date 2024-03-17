DROP TABLE IF EXISTS appuser;
DROP TABLE IF EXISTS file_record;
DROP TABLE IF EXISTS basic_information;
DROP TABLE IF EXISTS digital_object;
DROP TABLE IF EXISTS resource_types;
DROP TABLE IF EXISTS pid_log;

CREATE TABLE appuser
(
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT        NOT NULL,
    last_name  TEXT        NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    password   TEXT        NOT NULL
);

CREATE TABLE file_record
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name      TEXT,
    file_path      TEXT,
    file_extension TEXT,
    upload_date    TEXT
);

CREATE TABLE basic_information
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT,
    pub_date         TEXT,
    doi              TEXT,
    docid_doi        TEXT,
    resource_type_id INTEGER,
    description      TEXT,
    family_name      TEXT,
    given_name       TEXT,
    identifier       TEXT,
    affiliation      TEXT,
    role             TEXT,
    file_id          INTEGER,
    FOREIGN KEY (resource_type_id) REFERENCES resource_types (id),
    FOREIGN KEY (file_id) REFERENCES file_record (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE digital_object
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name        TEXT,
    file_path        TEXT,
    file_extension   TEXT,
    upload_date      TEXT,
    title            TEXT,
    pub_date         TEXT,
    doi              TEXT,
    docid_doi        TEXT,
    resource_type_id INTEGER,
    description      TEXT,
    creator_type     TEXT,
    family_name      TEXT,
    given_name       TEXT,
    identifier       TEXT,
    affiliation      TEXT,
    role             TEXT,
    FOREIGN KEY (resource_type_id) REFERENCES resource_types (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

-- Create creators table 1 to N

-- Create the resource_types lookup table
CREATE TABLE resource_types
(
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Insert the predefined resource types into the lookup table
INSERT INTO resource_types (name)
VALUES ('Dataset'),
       ('Event'),
       ('Image'),
       ('Image / Diagram'),
       ('Image / Drawing'),
       ('Image / Figure'),
       ('Image / Other'),
       ('Image / Photo'),
       ('Image / Plot'),
       ('Lesson'),
       ('Model'),
       ('Other'),
       ('Physical object'),
       ('Poster'),
       ('Presentation'),
       ('Publication'),
       ('Publication / Annotation collection'),
       ('Publication / Book'),
       ('Publication / Book chapter'),
       ('Publication / Conference paper'),
       ('Publication / Conference proceeding'),
       ('Publication / Data paper'),
       ('Publication / Dissertation'),
       ('Publication / Journal'),
       ('Publication / Journal article'),
       ('Publication / Other'),
       ('Publication / Output management plan'),
       ('Publication / Patent'),
       ('Publication / Peer review'),
       ('Publication / Preprint'),
       ('Publication / Project deliverable'),
       ('Publication / Project milestone'),
       ('Publication / Proposal'),
       ('Publication / Report'),
       ('Publication / Software documentation'),
       ('Publication / Standard'),
       ('Publication / Taxonomic treatment'),
       ('Publication / Technical note'),
       ('Publication / Thesis'),
       ('Publication / Working paper'),
       ('Software'),
       ('Software / Computational notebook'),
       ('Video/Audio'),
       ('Workflow');

-- For retrieving DOCID and assigning it to a document object
CREATE TABLE pid_log
(
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL,
    description       TEXT NOT NULL,
    pid               TEXT NOT NULL UNIQUE,
    pid_reserved      INTEGER,
    pid_reserved_date TEXT,
    pid_reserved_by   TEXT,
    pid_assigned      INTEGER,
    pid_assigned_date TEXT,
    pid_assigned_by   TEXT,
    object_ref        TEXT
);

-- Define a recursive generation of series of numbers from 1 to 100
WITH RECURSIVE series(n) AS (SELECT 1
                             UNION ALL
                             SELECT n + 1
                             FROM series
                             WHERE n < 100)

-- Insert records into the pid_log table with unique pid values
INSERT
INTO pid_log (name, description, pid, pid_reserved, pid_reserved_date, pid_reserved_by, pid_assigned, pid_assigned_date,
pid_assigned_by, object_ref)
SELECT 'Sample PID ' || printf('%04d', n),
       'DOCID Sample',
       '20.' || printf('%04d', n) || '/' || printf('%04d', n),
       NULL,
       NULL,
       NULL,
       NULL,
       NULL,
       NULL,
       NULL
FROM series;
