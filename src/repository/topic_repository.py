from typing import Optional
from model import Topic


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