from typing import Optional
from model import Book, PersistedScore, Review, Score, Topic

class TopicRepository:

    def __init__(self, con):
        self.con = con

    def add(self, topic):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO topic (
                        t_id,
                        t_description) VALUES (
                        ?,?)"""

            cur.execute(
                query,
                (
                    None,
                    topic.description,
                )
            )

            return cur.lastrowid

    def delete(self, id):
        with self.con:
            cur = self.con.cursor()
            query = "DELETE FROM topic WHERE t_id = ?"

            cur.execute(query, (id,))

    def get_all(self) -> list[Topic]:
        with self.con:
            cur = self.con.cursor()
            query = "SELECT t_description FROM topic"

            return [Topic(c[0]) for c in cur.execute(query).fetchall()]

    def get_by_id(self, id) -> Optional[Topic]:
        with self.con:
            cur = self.con.cursor()
            query = "SELECT t_description FROM topic WHERE t_id = ?"
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Topic(result[0])
            return None

class BookRepository:

    def __init__(self, con):
        self.con = con


    def add(self, book, topic):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO book (
                        b_id,
                        b_author,
                        b_title,
                        b_pub_date,
                        b_topic) VALUES (
                        ?,?,?,?,?)"""

            cur.execute(
                query,
                (
                    None,
                    book.author,
                    book.title,
                    book.publication_date,
                    topic,
                ) )

            return cur.lastrowid

    def update(self, book, id):
        with self.con:
            cur = self.con.cursor()
            query = """UPDATE book SET
                        b_author = ?,
                        b_title = ?,
                        b_pub_date = ?
                        WHERE b_id = ?"""

            cur.execute(
                query,
                (
                    book.author,
                    book.title,
                    book.publication_date,
                    id,
                ) )

    def delete(self, id):
        with self.con:
            cur = self.con.cursor()
            query = "DELETE FROM book WHERE b_id = ?"

            cur.execute(query, (id,))

    def get_all(self, topic_id) -> list[Book]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        b_author,
                        b_title,
                        b_pub_date
                       FROM book WHERE b_topic = ?"""

            return [Book(author = b[0], title = b[1], publication_date = b[2]) for b in cur.execute(query, (topic_id,)).fetchall()]

    def get_by_id(self, id):
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        b_author,
                        b_title,
                        b_pub_date
                       FROM book WHERE b_id = ?"""

            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Book(result[0], result[1], result[2])
            return None

class ReviewRepository:

    def __init__(self, con):
        self.con = con

    def add(self, review, book):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO review (
                        r_id,
                        r_guest,
                        r_content,
                        r_book) VALUES (
                        ?,?,?,?)"""

            cur.execute(
                query,
                (
                    None,
                    review.guest,
                    review.content,
                    book,
                )
            )

            return cur.lastrowid

    def delete(self, id):
        with self.con:
            cur = self.con.cursor()
            query = "DELETE FROM review WHERE r_id = ?"

            cur.execute(query, (id,))

    def get_all(self, book_id) -> list[Review]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        r_guest,
                        r_content
                       FROM review WHERE r_book = ?"""

            return [Review(guest = r[0], content = r[1]) for r in cur.execute(query, (book_id,)).fetchall()]

    def get_by_id(self,id) -> Optional[Review]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        r_guest,
                        r_content
                        FROM review WHERE r_id = ?"""
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Review(guest = result[0], content = result[1])
            return None

class ScoreRepository:

    def __init__(self, con):
        self.con = con

    def add(self, score, book):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO score (
                        s_id,
                        s_guest,
                        s_value,
                        s_book) VALUES (
                        ?,?,?,?)"""

            cur.execute(
                query,
                (
                    None,
                    score.guest,
                    score.value,
                    book,
                ) )

            return cur.lastrowid

    def get_all(self, book_id):
        with self.con:
            cur = self.con.cursor()
            query = "SELECT s_id, s_value FROM score WHERE s_book = ?"

            return [PersistedScore(s[0], s[1]) for s in cur.execute(query, (book_id,)).fetchall()]