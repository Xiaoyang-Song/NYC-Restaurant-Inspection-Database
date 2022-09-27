-- Project 1 Relational Model
-- Contributor: Xiaoyang Song, Han Liu

-- Entity: User
CREATE TABLE User(
    userid int serial PRIMARY KEY,
    account_name text NOT NULL,
    passcode text NOT NULL,
    dob date,
    district text,
    CHECK (
        district IN ("Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island")
    )
)

CREATE TABLE Restaurant(
    rid int serial PRIMARY KEY,
    DBA text NOT NULL,
    phone_number VARCHAR(10),
    cuisine text
)

CREATE TABLE Grade(
    gid int serial PRIMARY KEY,
    grade CHAR(2) NOT NULL,
    score float,
    CHECK (
        grade in ('A', "B", 'C', 'P', 'Z')
    )
)

CREATE TABLE Inspection(
    iid int serial PRIMARY KEY,
    i_type text,
)

CREATE TABLE Violation(
    vid int serial PRIMARY KEY,
    code text,
    v_description text,
    critical_flag text,
    CHECK (
        critical_flag IN ("Critical", "Not Critical", "Not Applicable")
    )
)

CREATE TABLE Location(
    lid int serial PRIMARY KEY,
    district text,
    zipcode VARCHAR(5),
    street text,
    building text,
    CHECK (
        district IN ("Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island")
    )
)

CREATE TABLE Reviews_Post_Have(
    rev_id int serial PRIMARY KEY,
    content text,
    rev_time DATE,
    userid int NOT NULL,
    rid int NOT NULL,
    FOREIGN KEY (userid) REFERENCES User ON DELETE CASCADE,
    FOREIGN KEY (rid) REFERENCES Restaurant ON DELETE CASCADE
)

CREATE TABLE Locate(
    rid int REFERENCES Restaurant,
    lid int REFERENCES Location,
    NOT NULL lid,
    PRIMARY KEY rid
)

CREATE TABLE Feel(
    userid int NOT NULL,
    rid int NOT NULL,
    feel text NOT NULL,
    hate_time DATE,
    PRIMARY KEY (userid, rid),
    FOREIGN KEY (userid) REFERENCES User,
    FOREIGN KEY (rid) REFERENCES Restaurant,
    CHECK (
        feel IN ("Like", "Dislike")
    )
)

CREATE TABLE Graded(
    rid int NOT NULL,
    gid int NOT NULL,
    g_time DATE,
    PRIMARY KEY (rid, gid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (gid) REFERENCES Grade
)

CREATE TABLE Inspect(
    rid int NOT NULL,
    iid int NOT NULL,
    i_time DATE,
    PRIMARY KEY (rid, iid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (iid) REFERENCES Inspection
)

CREATE TABLE Violate(
    rid int NOT NULL,
    vid int NOT NULL,
    PRIMARY KEY (rid, vid),
    FOREIGN KEY (rid) REFERENCES Restaurant,
    FOREIGN KEY (vid) REFERENCES Violation
)

CREATE TABLE Found(
    iid int NOT NULL,
    vid int NOT NULL,
    PRIMARY KEY (iid, vid),
    FOREIGN KEY (iid) REFERENCES Inspection,
    FOREIGN KEY (vid) REFERENCES Violation
)


