import sqlite3
import unittest
import os

from flask import current_app, json
from api import app, init_repositories, init_services
from model import Book, Theme
from test.util import random_string

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("blog_unit_test.db")
        cls.cur = cls.conn.cursor()

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.client = app.test_client()

        repositories = init_repositories(cls.conn)
        services = init_services(repositories)

        app.config["services"] = services

        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

        if os.path.exists("blog_unit_test.db"):
            os.remove("blog_unit_test.db")

        cls.app_context.pop()

    def tearDown(self):
        self.cur.execute("DELETE FROM theme")
        self.conn.commit()

    def test_get_themes(self):
        t = Theme(random_string())

        service = current_app.config["services"]["theme"]
        service.add_theme(t)

        response = TestAPI.client.get('/themes')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn(t.description, data[0].values())

    def test_create_theme(self):
        payload = {"description": "science"}

        response = TestAPI.client.post(
            "/themes",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        app.logger.info(response.get_json())

        self.assertEqual(response.status_code, 201)
        self.assertIn("created_id", response.get_json())

    def test_get_books(self):
        t = Theme("history")
        theme_id = current_app.config["services"]["theme"].add_theme(t)

        b = Book(author = "Marguerite Yourcenar", title = "Memoirs of Hadrian", publication_year = 1954)
        current_app.config["services"]["book"].add_book(b, theme_id)

        response = TestAPI.client.get(f"/books/{theme_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertIn("Memoirs of Hadrian", data[0].values())