-- Project 1 Relational Model
-- Contributor: Xiaoyang Song, Han Liu

--DROP TABLE 
DROP TABLE IF EXISTS Graded, Grade, Feel, Violate, Violation, Inspect, Inspection, 
           Reviews_Post_Own, Users, Restaurant, Locations;
CREATE TABLE IF NOT EXISTS Users(
    userid serial PRIMARY KEY,
    account_name text NOT NULL,
    passcode text NOT NULL,
    dob date,
    district text,
    CHECK (
        district IN ('Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island')
    )
);

-- Entity: Locations
CREATE TABLE IF NOT EXISTS Locations(
    lid serial PRIMARY KEY,
    district text,
    zipcode VARCHAR(5),
    street text,
    building text,
    CHECK (
        district IN ('Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island')
    )
);
CREATE TABLE IF NOT EXISTS Restaurant(
    rid serial PRIMARY KEY,
    DBA text NOT NULL, -- DBA stands for "Doing Business As" (Acronym)
    phone_number VARCHAR(10), 
    cuisine text,
    lid int NOT NULL,
    FOREIGN KEY (lid) REFERENCES Locations
);

-- Entity: Grade
CREATE TABLE IF NOT EXISTS Grade(
    gid serial PRIMARY KEY,
    grade CHAR(1) NOT NULL,
    score float,
    CHECK (
        grade in ('A', 'B', 'C', 'P', 'N', 'Z')
    )
);
-- Entity: Inspection
CREATE TABLE IF NOT EXISTS Inspection(
    iid serial PRIMARY KEY,
    i_type text
);

-- Entity: Violation
CREATE TABLE IF NOT EXISTS Violation(
    vid serial PRIMARY KEY,
    code text,
    v_description text,
    critical_flag text,
    CHECK (
        critical_flag IN ('Critical', 'Not Critical', 'Not Applicable')
    )
);

-- Combine relationship sets and entity sets to model weak entity
CREATE TABLE IF NOT EXISTS Reviews_Post_Own(
    rev_id serial PRIMARY KEY,
    content text NOT NULL,
    post_time DATE,
    userid int NOT NULL,
    rid int NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES Restaurant ON DELETE CASCADE
);

-- Relationship sets: note that when translating to relational schema
-- We combine Like and Dislike into Feel to make things more efficient
CREATE TABLE IF NOT EXISTS Feel(
    userid int NOT NULL,
    rid int NOT NULL,
    feel text NOT NULL,
    PRIMARY KEY (userid, rid),
    FOREIGN KEY (userid) REFERENCES Users,
    FOREIGN KEY (rid) REFERENCES Restaurant,
    CHECK (
        feel IN ('Like', 'Dislike')
    )
);

-- Relationship set: Graded
CREATE TABLE IF NOT EXISTS Graded(
    rid int NOT NULL,
    gid int NOT NULL,
    g_time DATE,
    PRIMARY KEY (rid, gid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (gid) REFERENCES Grade
);

-- Relationship Set: Inspect
CREATE TABLE IF NOT EXISTS Inspect(
    rid int NOT NULL,
    iid int NOT NULL,
    i_time DATE NOT NULL,
    PRIMARY KEY (rid, iid, i_time),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (iid) REFERENCES Inspection
);

-- Relationship Set: Violate
CREATE TABLE IF NOT EXISTS Violate(
    rid int NOT NULL,
    vid int NOT NULL,
    v_time DATE NOT NULL,
    PRIMARY KEY (rid, vid, v_time),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (vid) REFERENCES Violation
);