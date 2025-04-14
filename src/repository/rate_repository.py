from model import Rate


class RateRepository:

    def __init__(self, con):
        self.con = con

    def add(self, rate, book):
        with self.con:
            cur = self.con.cursor()
            query = """INSERT INTO rate (
                        rt_id,
                        rt_guest,
                        rt_value,
                        rt_book) VALUES (
                        ?,?,?,?)"""

            cur.execute(
                query,
                (
                    None,
                    rate.guest,
                    rate.value,
                    book,
                ) )

            return cur.lastrowid

    def get_all(self):
        with self.con:
            cur = self.con.cursor()
            query = "SELECT rt_guest, rt_value FROM rate"

            return [Rate(guest = rt[0], value = rt[1]) for rt in cur.execute(query).fetchall()]