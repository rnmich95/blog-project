import unittest

from flask import json
from jsonschema import ValidationError

from api import validate_and_build
from model import Book, Review, Theme

class ValidationTest(unittest.TestCase):
    def test_validate_theme_from_json(self):
        d = """{"description": "fantasy"}"""

        expected = Theme("fantasy")
        self.assertEqual(expected, validate_and_build(Theme, json.loads(d)))

    def test_invalidate_theme_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Theme, json.loads(d))

    def test_validate_book_from_json(self):
        d = """{"author": "J. K. Rowling",
                "title": "Harry Potter and the Philosopher's Stone",
                "publication_year": "1997",
                "theme_id": 1}"""

        expected = Book("J. K. Rowling", "Harry Potter and the Philosopher's Stone", "1997", 1)
        self.assertEqual(expected, validate_and_build(Book, json.loads(d)))

    def test_invalidate_book_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Book, json.loads(d))

    def test_validate_review_from_json(self):
        d = """{"guest": "mich",
                "content": "This book sucks.",
                "book_id": 5}"""

        expected = Review("mich", "This book sucks.", 5)
        self.assertEqual(expected, validate_and_build(Review, json.loads(d)))

    def test_invalidate_review_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Review, json.loads(d))