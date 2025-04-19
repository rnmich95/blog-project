import sqlite3
import unittest

from flask import json
from api import app, init_repositories, init_services

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")

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

        # should I clean up test db ?

        cls.app_context.pop()

    def test_create_topic(self):
        payload = {"description": "Test 2"}

        response = TestAPI.client.post(
            "/topics",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        app.logger.info(response.get_json())

        self.assertEqual(response.status_code, 201)
        self.assertIn("lastrowid", response.get_json())