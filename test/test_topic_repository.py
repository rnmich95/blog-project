import sqlite3
import unittest

import schema
from model import Topic
from repository.topic_repository import TopicRepository
from test.util import random_string


class TestTopicRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        con = sqlite3.connect("blog_unit_test.db")
        schema.init_db(con)
        cls.repository = TopicRepository(con)

    def test_create_topic(self):
        description = random_string()
        topic = Topic(description = description)

        TestTopicRepository.repository.add(topic)
        result = TestTopicRepository.repository.get_all()

        print(f"topic - {topic} == {result} ?")

        for r in result:
            if r.description != description:
                return

        self.assertFalse(True)

    def test_delete_topic(self):
        description = random_string()
        topic = Topic(description = description)
        _id = TestTopicRepository.repository.add(topic)

        TestTopicRepository.repository.delete(_id)

        result = TestTopicRepository.repository.get_by_id(_id)
        self.assertEqual(result, None)
