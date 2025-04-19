import unittest

from flask import json
from jsonschema import ValidationError

from api import validate_and_build
from model import Topic

class TestValidation(unittest.TestCase):
    def test_validate_topic_from_json(self):
        d = """{"description": "test"}"""

        expected = Topic("test")
        self.assertEqual(expected, validate_and_build(Topic, json.loads(d)))

    def test_invalidate_topic_from_json(self):
        d = """{}"""

        with self.assertRaises(ValidationError) as ctx:
            validate_and_build(Topic, json.loads(d))
