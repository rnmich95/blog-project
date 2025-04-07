import sqlite3
import sys


def init_db(con):
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS topic")
    cur.execute("""CREATE TABLE IF NOT EXISTS topic (
        t_id INTEGER PRIMARY KEY,
        t_hint TEXT UNIQUE NOT NULL
        );""")

    cur.execute("DROP TABLE IF EXISTS book")
    cur.execute("""CREATE TABLE IF NOT EXISTS book (
                b_id INTEGER PRIMARY KEY,
                b_title TEXT NOT NULL,
                b_author TEXT NOT NULL,
                b_topic INTEGER NOT NULL,
                FOREIGN KEY(b_topic) REFERENCES topic(t_id)
                );""")

    cur.execute("DROP TABLE IF EXISTS review")
    cur.execute("""CREATE TABLE IF NOT EXISTS review (
                rv_id INTEGER PRIMARY KEY,
                rv_guest TEXT NOT NULL,
                rv_content TEXT NOT NULL,
                rv_book INTEGER NOT NULL,
                FOREIGN KEY(rv_book) REFERENCES book(b_id)
                );""")

    cur.execute("DROP TABLE IF EXISTS rate")
    cur.execute("""CREATE TABLE IF NOT EXISTS rate (
                rt_id INTEGER PRIMARY KEY,
                rt_guest TEXT NOT NULL,
                rt_value INTEGER NOT NULL,
                rt_book INTEGER NOT NULL,
                CHECK (rt_value > 0 AND rt_value <= 5),
                FOREIGN KEY(rt_book) REFERENCES book(b_id)
                );""")


if __name__ == '__main__':
    con = sqlite3.connect(sys.argv[1])
    init_db(con)
    con.close()