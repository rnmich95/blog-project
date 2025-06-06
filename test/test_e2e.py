import random
import sqlite3
import unittest
import os

from flask import current_app, json
from api import api
from main import app, init_repositories, init_services
from model import Book, Review, Score, Theme
from test.util import random_string

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("unit_test.db")
        cls.cur = cls.conn.cursor()

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.client = app.test_client()

        repositories = init_repositories(cls.conn)
        services = init_services(repositories)

        app.config["services"] = services

        app.register_blueprint(api)

        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

        if os.path.exists("unit_test.db"):
            os.remove("unit_test.db")

        cls.app_context.pop()

    """ def tearDown(self):
         self.cur.execute("DELETE FROM theme")
         self.conn.commit() """

    def test_get_themes(self):
        t = Theme(random_string())

        service = current_app.config["services"]["theme"]
        service.add_theme(t)

        response = TestAPI.client.get("/themes")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        for d in data:
            if d["description"] == t.description:
                return

        self.assertFalse(True)

    def test_create_theme(self):
        description = random_string()
        payload = {"description": description}

        response = TestAPI.client.post(
            "/themes",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("created_id", response.get_json())

    def test_get_books(self):
        t = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(t)

        b = Book(author = random_string(), title = random_string(), publication_year = random_string(), theme_id = theme_id)
        current_app.config["services"]["book"].add_book(b)

        response = TestAPI.client.get(f"/books/{theme_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        for d in data:
            if d["author"] == b.author and \
               d["title"] == b.title and \
               d["publication_year"] == b.publication_year and \
               d["theme_id"] == b.theme_id:
                return

        self.assertFalse(True)

    def test_create_book(self):
        t = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(t)

        payload = {"author": random_string(),
                   "title": random_string(),
                   "publication_year": random_string(),
                   "theme_id": theme_id}

        response = TestAPI.client.post(
            f"/books/{theme_id}",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("created_id", response.get_json())

    def test_update_book(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book =  Book(author = random_string(),
                     title = random_string(),
                     publication_year = random_string(),
                     theme_id = theme_id )

        book_id = current_app.config["services"]["book"].add_book(book)

        payload = {"author": random_string(),
                   "title": random_string(),
                   "publication_year": random_string(),
                   "theme_id": theme_id }

        response = TestAPI.client.put(
            f"/books/{book_id}",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id )
        book_id = current_app.config["services"]["book"].add_book(book)

        response = TestAPI.client.delete(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_reviews(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id)
        book_id = current_app.config["services"]["book"].add_book(book)

        review = Review(guest = random_string(),
                        content = random_string(),
                        book_id = book_id)
        current_app.config["services"]["review"].add_review(review)

        response = TestAPI.client.get(f"/reviews/{book_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        for d in data:
            if d["guest"] == review.guest and \
               d["content"] == review.content and \
               d["book_id"] == review.book_id:

                return

        self.assertFalse(True)

    def test_create_review(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id)
        book_id = current_app.config["services"]["book"].add_book(book)

        payload = {"guest": random_string(),
                   "content": random_string(),
                   "book_id": book_id}

        response = TestAPI.client.post(
            f"/reviews/{book_id}",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("created_id", response.get_json())

    def test_delete_review(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id )
        book_id = current_app.config["services"]["book"].add_book(book)

        review = Review(guest = random_string(),
                        content = random_string(),
                        book_id = book_id)
        review_id = current_app.config["services"]["review"].add_review(review)

        response = TestAPI.client.delete(f"/reviews/{review_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_avarage_score(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id)
        book_id = current_app.config["services"]["book"].add_book(book)

        s1 = Score(guest = random_string(),
                   value = random.randint(1, 5),
                   book_id = book_id)
        current_app.config["services"]["score"].add_score(s1)

        s2 = Score(guest = random_string(),
                   value = random.randint(1, 5),
                   book_id = book_id)
        current_app.config["services"]["score"].add_score(s2)

        response = TestAPI.client.get(f"/overall_score/{book_id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        if data["overall_score"] == (s1.value + s2.value) / 2:
            return

        self.assertFalse(True)

    def test_add_score(self):
        theme = Theme(random_string())
        theme_id = current_app.config["services"]["theme"].add_theme(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string(),
                    theme_id = theme_id)
        book_id = current_app.config["services"]["book"].add_book(book)

        payload = {"guest": random_string(),
                   "value": random.randint(1, 5),
                   "book_id": book_id}

        response = TestAPI.client.post(
            f"/scores/{book_id}",
            data = json.dumps(payload),
            content_type = "application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("created_id", response.get_json())