from src.model.topic_model import Topic


class TopicRepository:

    def __init__(self, con):
        self.con = con

    def add(self, topic):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO topic (
                    t_id,
                    t_hint) VALUES (
                    ?,?)"""

            cur.execute(
                query,
                (
                    None,
                    topic.hint,
                )
            )

    def delete(self, topic):
        with self.con:
            cur = self.con.cursor()
            query = "DELETE FROM topic WHERE t_hint = ?"

            cur.execute(query, (topic,))

    def select(self) -> list[Topic]:
        with self.con:
            cur = self.con.cursor()
            query = "SELECT t_hint FROM topic"

            return [Topic(hint=c[0]) for c in cur.execute(query).fetchall()]
