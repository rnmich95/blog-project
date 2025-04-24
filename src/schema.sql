CREATE TABLE IF NOT EXISTS theme (
    t_id INTEGER PRIMARY KEY,
    t_description TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS book (
    b_id INTEGER PRIMARY KEY,
    b_author TEXT NOT NULL,
    b_title TEXT UNIQUE NOT NULL,
    b_pub_year TEXT NOT NULL,
    b_theme INTEGER NOT NULL,
    FOREIGN KEY(b_theme) REFERENCES theme(t_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS review (
    r_id INTEGER PRIMARY KEY,
    r_guest TEXT NOT NULL,
    r_content TEXT NOT NULL,
    r_book INTEGER NOT NULL,
    FOREIGN KEY(r_book) REFERENCES book(b_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS score (
    s_id INTEGER PRIMARY KEY,
    s_guest TEXT NOT NULL,
    s_value INTEGER NOT NULL,
    s_book INTEGER NOT NULL,
    CHECK (s_value > 0 AND s_value <= 5),
    FOREIGN KEY(s_book) REFERENCES book(b_id) ON DELETE CASCADE,
    UNIQUE(s_guest, s_book)
);