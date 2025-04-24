from typing import Optional
from model import Book, PersistedBook, PersistedScore, Review, Score, Theme

class ThemeRepository:

    def __init__(self, conn):
        self.conn = conn

    def add(self, theme):
        with self.conn:
            cur = self.conn.cursor()
            query = """INSERT INTO theme (
                        t_id,
                        t_description) VALUES (
                        ?,?)"""

            cur.execute(
                query,
                (
                    None,
                    theme.description,
                )
            )

            created_id = cur.lastrowid

            return created_id

    def delete(self, id):
        with self.conn:
            cur = self.conn.cursor()
            query = "DELETE FROM theme WHERE t_id = ?"

            cur.execute(query, (id,))

    def get_all(self) -> list[Theme]:
        with self.conn:
            cur = self.conn.cursor()
            query = "SELECT t_description FROM theme"

            return [Theme(c[0]) for c in cur.execute(query).fetchall()]

    def get_by_id(self, id) -> Optional[Theme]:
        with self.conn:
            cur = self.conn.cursor()
            query = "SELECT t_description FROM theme WHERE t_id = ?"
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Theme(result[0])
            return None

class BookRepository:

    def __init__(self, conn):
        self.conn = conn


    def add(self, book, theme):
        with self.conn:
            cur = self.conn.cursor()
            query = """INSERT INTO book (
                        b_id,
                        b_author,
                        b_title,
                        b_pub_year,
                        b_theme) VALUES (
                        ?,?,?,?,?)"""

            cur.execute(
                query,
                (
                    None,
                    book.author,
                    book.title,
                    book.publication_year,
                    theme,
                ) )

            created_id = cur.lastrowid

            return created_id

    def update(self, book, id):
        with self.conn:
            cur = self.conn.cursor()
            query = """UPDATE book SET
                        b_author = ?,
                        b_title = ?,
                        b_pub_year = ?
                        WHERE b_id = ?"""

            cur.execute(
                query,
                (
                    book.author,
                    book.title,
                    book.publication_year,
                    id,
                ) )

    def delete(self, id):
        with self.conn:
            cur = self.conn.cursor()
            query = "DELETE FROM book WHERE b_id = ?"

            cur.execute(query, (id,))

    def get_all(self, theme_id) -> list[Book]:
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        b_author,
                        b_title,
                        b_pub_year,
                        b_theme
                       FROM book WHERE b_theme = ?"""

            return [PersistedBook(author = b[0], title = b[1], publication_year = b[2], theme_id = b[3]) for b in cur.execute(query, (theme_id,)).fetchall()]

    def get_by_id(self, id):
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        b_author,
                        b_title,
                        b_pub_year,
                        b_theme
                       FROM book WHERE b_id = ?"""

            result = cur.execute(query, (id,)).fetchone()

            if result:
                return PersistedBook(author = result[0], title = result[1], publication_year = result[2], theme_id = result[3])
            return None

class ReviewRepository:

    def __init__(self, conn):
        self.conn = conn

    def add(self, review, book):
        with self.conn:
            cur = self.conn.cursor()
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

            created_id = cur.lastrowid

            return created_id

    def delete(self, id):
        with self.conn:
            cur = self.conn.cursor()
            query = "DELETE FROM review WHERE r_id = ?"

            cur.execute(query, (id,))

    def get_all(self, book_id) -> list[Review]:
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        r_guest,
                        r_content
                       FROM review WHERE r_book = ?"""

            return [Review(guest = r[0], content = r[1]) for r in cur.execute(query, (book_id,)).fetchall()]

    def get_by_id(self,id) -> Optional[Review]:
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        r_guest,
                        r_content
                        FROM review WHERE r_id = ?"""
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Review(guest = result[0], content = result[1])
            return None

class ScoreRepository:

    def __init__(self, conn):
        self.conn = conn

    def add(self, score, book):
        with self.conn:
            cur = self.conn.cursor()
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

            created_id = cur.lastrowid

            return created_id

    def get_all(self, book_id):
        with self.conn:
            cur = self.conn.cursor()
            query = "SELECT s_id, s_value FROM score WHERE s_book = ?"

            return [PersistedScore(s[0], s[1]) for s in cur.execute(query, (book_id,)).fetchall()]