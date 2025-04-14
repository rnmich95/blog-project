import random
import sqlite3
import unittest

import schema
from model import Book, Rate, Topic
from test.util import random_string
from repository.rate_repository import RateRepository
from repository.book_repository import BookRepository
from repository.topic_repository import TopicRepository


class TestRateRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        con = sqlite3.connect("blog_unit_test.db")
        schema.init_db(con)
        cls.topicRepository = TopicRepository(con)
        cls.bookRepository = BookRepository(con)
        cls.rateRepository = RateRepository(con)

    def test_create_rate(self):
        topic = Topic(description = random_string())
        topic_id = TestRateRepository.topicRepository.add(topic)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string() )
        book_id = TestRateRepository.bookRepository.add(book, topic_id)

        guest = random_string()
        value = random.randint(1,5)

        rate = Rate(guest,value)
        TestRateRepository.rateRepository.add(rate, book_id)

        result = TestRateRepository.rateRepository.get_all()
        for rt in result:
            if rt.guest == guest and rt.value == value:
                return

        self.assertFalse(True)