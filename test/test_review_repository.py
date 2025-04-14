import sqlite3
import unittest

from model import Book, Review, Topic
import schema
from test.util import random_string
from repository.book_repository import BookRepository
from repository.topic_repository import TopicRepository
from repository.review_repository import ReviewRepository


class TestReviewRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        con = sqlite3.connect("blog_unit_test.db")
        schema.init_db(con)
        cls.topicRepository = TopicRepository(con)
        cls.bookRepository = BookRepository(con)
        cls.reviewRepository = ReviewRepository(con)

    def test_create_review(self):
        topic = Topic(description = random_string())
        topic_id = TestReviewRepository.topicRepository.add(topic)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string() )
        book_id = TestReviewRepository.bookRepository.add(book, topic_id)

        guest = random_string()
        content = random_string()

        review = Review(guest = guest, content = content)
        TestReviewRepository.reviewRepository.add(review, book_id)

        result = TestReviewRepository.reviewRepository.get_all()

        for rv in result:
            if rv.guest == guest and \
               rv.content == content:

                return

        self.assertFalse(True)

    def test_delete_review(self):
        topic = Topic(description = random_string())
        topic_id = TestReviewRepository.topicRepository.add(topic)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string() )
        book_id = TestReviewRepository.bookRepository.add(book, topic_id)

        guest = random_string()
        content = random_string()

        review = Review(guest = guest, content = content)
        review_id = TestReviewRepository.reviewRepository.add(review, book_id)

        TestReviewRepository.reviewRepository.delete(review_id)

        result = TestReviewRepository.reviewRepository.get_by_id(review_id)

        self.assertEqual(result, None)