from typing import Optional
from model import Review


class ReviewRepository:

    def __init__(self, con):
        self.con = con

    def add(self, review, book):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO review (
                        rv_id,
                        rv_guest,
                        rv_content,
                        rv_book) VALUES (
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
            query = "DELETE FROM review WHERE rv_id = ?"

            cur.execute(query, (id,))

    def get_all(self) -> list[Review]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        rv_guest,
                        rv_content
                       FROM review"""

            return [Review(guest = rv[0], content = rv[1]) for rv in cur.execute(query).fetchall()]

    def get_by_id(self,id) -> Optional[Review]:
        with self.con:
            cur = self.con.cursor()
            query = """SELECT
                        rv_guest,
                        rv_content
                        FROM review WHERE rv_id = ?"""
            result = cur.execute(query, (id,)).fetchone()

            if result:
                return Review(guest = result[0], content = result[1])
            return None
