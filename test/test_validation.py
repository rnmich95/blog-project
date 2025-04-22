import unittest

from flask import json
from jsonschema import ValidationError

from api import validate_and_build
from model import Book, Topic

class TestValidation(unittest.TestCase):
    def test_validate_topic_from_json(self):
        d = """{"description": "fantasy"}"""

        expected = Topic("fantasy")
        self.assertEqual(expected, validate_and_build(Topic, json.loads(d)))

    def test_invalidate_topic_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Topic, json.loads(d))

    def test_validate_book_from_json(self):
        d = """{"author": "J. K. Rowling",
                "title": "Harry Potter and the Philosopher's Stone",
                "publication_date": "June 1997"}"""

        expected = Book("J. K. Rowling", "Harry Potter and the Philosopher's Stone", "June 1997")
        self.assertEqual(expected, validate_and_build(Book, json.loads(d)))

    def test_invalidate_book_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Book, json.loads(d))