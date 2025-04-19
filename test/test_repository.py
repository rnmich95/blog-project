import random
import sqlite3
import unittest

from model import Book, Review, Score, Topic
from repository import BookRepository, ReviewRepository, ScoreRepository, TopicRepository
from test.util import random_string

# create a separate class for database set up and tear down
class TestTopicRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.con.executescript(schema_script)

        cls.repository = TopicRepository(cls.con)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_create_topic(self):
        description = random_string()
        topic = Topic(description = description)

        TestTopicRepository.repository.add(topic)
        result = TestTopicRepository.repository.get_all()

        for r in result:
            if r.description == description:
                return

        self.assertFalse(True)

    def test_delete_topic(self):
        description = random_string()
        topic = Topic(description = description)
        _id = TestTopicRepository.repository.add(topic)

        TestTopicRepository.repository.delete(_id)

        result = TestTopicRepository.repository.get_by_id(_id)
        self.assertEqual(result, None)

class TestBookRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.con.executescript(schema_script)

        cls.bookRepository  = BookRepository(cls.con)
        cls.topicRepository = TopicRepository(cls.con)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_create_book(self):
        author = random_string()
        title  = random_string()
        publication_date = random_string()
        book   = Book(author = author,
                      title = title,
                      publication_date = publication_date )

        description = random_string()
        topic  = Topic(description = description)

        topic_id = TestBookRepository.topicRepository.add(topic)

        TestBookRepository.bookRepository.add(book, topic_id)
        result = TestBookRepository.bookRepository.get_all(topic_id)

        for b in result:
            if b.author == author and \
               b.title == title and \
               b.publication_date == publication_date:

                return

        self.assertFalse(True)

    def test_update_book(self):
        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string() )

        print(book.publication_date)

        topic = Topic(description = random_string())

        topic_id = TestBookRepository.topicRepository.add(topic)
        book_id = TestBookRepository.bookRepository.add(book, topic_id)

        author = random_string()
        title = random_string()
        publication_date = random_string()

        new_book = Book(author = author,
                        title = title,
                        publication_date = publication_date )

        print(new_book.publication_date)

        TestBookRepository.bookRepository.update(new_book, book_id)
        result = TestBookRepository.bookRepository.get_by_id(book_id)

        if result.author == author and \
           result.title == title and \
           result.publication_date == publication_date:

            return

        self.assertFalse(True)

    def test_delete_book(self):
        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string())

        topic = Topic(description = random_string())

        topic_id = TestBookRepository.topicRepository.add(topic)
        book_id = TestBookRepository.bookRepository.add(book, topic_id)

        TestBookRepository.bookRepository.delete(book_id)

        result = TestBookRepository.bookRepository.get_by_id(book_id)
        self.assertEqual(result, None)

class TestReviewRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.con.executescript(schema_script)

        cls.topicRepository  = TopicRepository(cls.con)
        cls.bookRepository   = BookRepository(cls.con)
        cls.reviewRepository = ReviewRepository(cls.con)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

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

        result = TestReviewRepository.reviewRepository.get_all(book_id)

        for r in result:
            if r.guest == guest and \
               r.content == content:

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

class TestScoreRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.con.executescript(schema_script)

        cls.topicRepository = TopicRepository(cls.con)
        cls.bookRepository  = BookRepository(cls.con)
        cls.scoreRepository = ScoreRepository(cls.con)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_create_score(self):
        topic = Topic(description = random_string())
        topic_id = TestScoreRepository.topicRepository.add(topic)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_date = random_string() )
        book_id = TestScoreRepository.bookRepository.add(book, topic_id)

        guest = random_string()
        value = random.randint(1,5)

        score = Score(guest,value)
        score_id = TestScoreRepository.scoreRepository.add(score, book_id)

        result = TestScoreRepository.scoreRepository.get_all(book_id)
        for s in result:
            if s._id == score_id and s.value == value:
                return

        self.assertFalse(True)
