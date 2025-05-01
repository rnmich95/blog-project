from typing import Optional
from model import Book, PersistedBook, PersistedReview, PersistedScore, PersistedTheme, Review, Score, Theme

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
            query = "SELECT t_id, t_description FROM theme"

            return [PersistedTheme(_id = t[0], description = t[1]) for t in cur.execute(query).fetchall()]

    def get_by_id(self, id) -> Optional[Theme]:
        with self.conn:
            cur = self.conn.cursor()
            query = "SELECT t_id, t_description FROM theme WHERE t_id = ?"
            t = cur.execute(query, (id,)).fetchone()

            if t:
                return PersistedTheme(t[0], t[1])
            return None

class BookRepository:

    def __init__(self, conn):
        self.conn = conn


    def add(self, book):
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
                    book.theme_id,
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
                        b_id,
                        b_author,
                        b_title,
                        b_pub_year,
                        b_theme
                       FROM book WHERE b_theme = ?"""

            return [PersistedBook(_id = b[0], author = b[1], title = b[2], publication_year = b[3], theme_id = b[4]) for b in cur.execute(query, (theme_id,)).fetchall()]

    def get_by_id(self, id):
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        b_id,
                        b_author,
                        b_title,
                        b_pub_year,
                        b_theme
                       FROM book WHERE b_id = ?"""

            result = cur.execute(query, (id,)).fetchone()

            if result:
                return PersistedBook(_id = result[0], author = result[1], title = result[2], publication_year = result[3], theme_id = result[4])
            return None

class ReviewRepository:

    def __init__(self, conn):
        self.conn = conn

    def add(self, review):
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
                    review.book_id,
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
                        r_id,
                        r_guest,
                        r_content,
                        r_book
                       FROM review WHERE r_book = ?"""

            return [PersistedReview(_id = r[0], guest = r[1], content = r[2], book_id = r[3]) for r in cur.execute(query, (book_id,)).fetchall()]

    def get_by_id(self,id) -> Optional[Review]:
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        r_id,
                        r_guest,
                        r_content,
                        r_book
                        FROM review WHERE r_id = ?"""
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return PersistedReview(_id = result[0], guest = result[1], content = result[2], book_id = result[3])
            return None

class ScoreRepository:

    def __init__(self, conn):
        self.conn = conn

    def add(self, score):
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
                    score.book_id,
                ) )

            created_id = cur.lastrowid

            return created_id

    def get_all(self, book_id):
        with self.conn:
            cur = self.conn.cursor()
            query = """SELECT
                        s_id,
                        s_guest,
                        s_value,
                        s_book
                       FROM score WHERE s_book = ?"""

            return [PersistedScore(_id = s[0], guest = s[1], value = s[2], book_id = s[3]) for s in cur.execute(query, (book_id,)).fetchall()]