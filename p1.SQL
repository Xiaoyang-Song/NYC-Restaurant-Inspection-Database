-- Project 1 Relational Model
-- Contributor: Xiaoyang Song, Han Liu

-- Entity: User
CREATE TABLE Users(
    userid serial PRIMARY KEY,
    account_name text NOT NULL,
    passcode text NOT NULL,
    dob date,
    district text,
    CHECK (
        district IN ('Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island')
    )
);

-- Entity: Restaurant
-- Note that for phone_number, we focus on US phone number only.
CREATE TABLE Restaurant(
    rid serial PRIMARY KEY,
    DBA text NOT NULL, -- DBA stands for "Doing Business As" (Acronym)
    phone_number VARCHAR(10), 
    cuisine text
);

-- Entity: Grade
CREATE TABLE Grade(
    gid serial PRIMARY KEY,
    grade CHAR(1) NOT NULL,
    score float,
    CHECK (
        grade in ('A', 'B', 'C', 'P', 'Z')
    )
);

-- Entity: Inspection
CREATE TABLE Inspection(
    iid serial PRIMARY KEY,
    i_type text
);

-- Entity: Violation
CREATE TABLE Violation(
    vid serial PRIMARY KEY,
    code text,
    v_description text,
    critical_flag text,
    CHECK (
        critical_flag IN ('Critical', 'Not Critical', 'Not Applicable')
    )
);

-- Entity: Locations
CREATE TABLE Locations(
    lid serial PRIMARY KEY,
    district text,
    zipcode VARCHAR(5),
    street text,
    building text,
    CHECK (
        district IN ('Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island')
    )
);

-- Combine relationship sets and entity sets to model weak entity
CREATE TABLE Reviews_Post_Have(
    rev_id serial PRIMARY KEY,
    content text NOT NULL,
    rev_time DATE,
    userid int NOT NULL,
    rid int NOT NULL,
    FOREIGN KEY (userid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES Restaurant ON DELETE CASCADE
);

-- Relationship sets
CREATE TABLE Locates(
    rid int PRIMARY KEY REFERENCES Restaurant,
    lid int NOT NULL REFERENCES Locations
);

-- Relationship sets: note that when translating to relational schema
-- We combine Like and Dislike into Feel to make things more efficient
CREATE TABLE Feel(
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
CREATE TABLE Graded(
    rid int NOT NULL,
    gid int NOT NULL,
    g_time DATE,
    PRIMARY KEY (rid, gid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (gid) REFERENCES Grade
);

-- Relationship Set: Inspect
CREATE TABLE Inspect(
    rid int NOT NULL,
    iid int NOT NULL,
    i_time DATE,
    PRIMARY KEY (rid, iid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (iid) REFERENCES Inspection
);

-- Relationship Set: Violate
CREATE TABLE Violate(
    rid int NOT NULL,
    vid int NOT NULL,
    PRIMARY KEY (rid, vid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (vid) REFERENCES Violation
);

-- Relationship Set: Found
CREATE TABLE Found(
    iid int NOT NULL,
    vid int NOT NULL,
    PRIMARY KEY (iid, vid),
    FOREIGN KEY (iid) REFERENCES Inspection,
    FOREIGN KEY (vid) REFERENCES Violation
);


