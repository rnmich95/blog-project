from model import Book


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

    def get_all(self) -> list[Book]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        b_author,
                        b_title,
                        b_pub_date
                       FROM book"""

            return [Book(author = b[0], title = b[1], publication_date = b[2]) for b in cur.execute(query).fetchall()]

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