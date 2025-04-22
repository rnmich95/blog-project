import sqlite3
import unittest
import os

from flask import current_app, json
from api import app, init_repositories, init_services
from model import Book, Topic

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")
        cls.cur = cls.con.cursor()

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.con.executescript(schema_script)

        cls.client = app.test_client()

        repositories = init_repositories(cls.con)
        services = init_services(repositories)

        app.config["services"] = services

        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

        if os.path.exists("blog_unit_test.db"):
            os.remove("blog_unit_test.db")

        cls.app_context.pop()

    def tearDown(self):
        self.cur.execute("DELETE FROM topic")
        self.con.commit()

    def test_get_topics(self):
        t = Topic("travel")

        service = current_app.config["services"]["topic"]
        service.add_topic(t)

        response = TestAPI.client.get('/topics')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertIn("travel", data[0].values())

    def test_create_topic(self):
        payload = {"description": "science"}

        response = TestAPI.client.post(
            "/topics",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        app.logger.info(response.get_json())

        self.assertEqual(response.status_code, 201)
        self.assertIn("lastrowid", response.get_json())

    def test_get_books(self):
        t = Topic("history")
        topic_id = current_app.config["services"]["topic"].add_topic(t)

        b = Book(author = "Marguerite Yourcenar", title = "Memoirs of Hadrian", publication_date = 1954)
        current_app.config["services"]["book"].add_book(b, topic_id)

        response = TestAPI.client.get(f"/books/{topic_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertIn("Memoirs of Hadrian", data[0].values())