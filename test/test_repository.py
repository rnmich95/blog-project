import random
import sqlite3
import unittest

from model import Book, Review, Score, Theme
from repository import BookRepository, ReviewRepository, ScoreRepository, ThemeRepository
from test.util import random_string

class ThemeRepositoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.repository = ThemeRepository(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_theme(self):
        description = random_string()
        theme = Theme(description = description)

        ThemeRepositoryTest.repository.add(theme)
        result = ThemeRepositoryTest.repository.get_all()

        for r in result:
            if r.description == description:
                return

        self.assertFalse(True)

    def test_delete_theme(self):
        description = random_string()
        theme = Theme(description = description)
        created_id = ThemeRepositoryTest.repository.add(theme)

        ThemeRepositoryTest.repository.delete(created_id)

        result = ThemeRepositoryTest.repository.get_by_id(created_id)
        self.assertEqual(result, None)

class BookRepositoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.book_repository  = BookRepository(cls.conn)
        cls.theme_repository = ThemeRepository(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_book(self):
        author = random_string()
        title  = random_string()
        publication_year = random_string()
        book   = Book(author = author,
                      title = title,
                      publication_year = publication_year )

        description = random_string()
        theme  = Theme(description = description)

        created_theme_id = BookRepositoryTest.theme_repository.add(theme)

        BookRepositoryTest.book_repository.add(book, created_theme_id)
        result = BookRepositoryTest.book_repository.get_all(created_theme_id)

        for b in result:
            if b.author == author and \
               b.title == title and \
               b.publication_year == publication_year:

                return

        self.assertFalse(True)

    def test_update_book(self):
        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string() )

        print(book.publication_year)

        theme = Theme(description = random_string())

        created_theme_id = BookRepositoryTest.theme_repository.add(theme)
        created_book_id = BookRepositoryTest.book_repository.add(book, created_theme_id)

        author = random_string()
        title = random_string()
        publication_year = random_string()

        new_book = Book(author = author,
                        title = title,
                        publication_year = publication_year )

        print(new_book.publication_year)

        BookRepositoryTest.book_repository.update(new_book, created_book_id)
        result = BookRepositoryTest.book_repository.get_by_id(created_book_id)

        if result.author == author and \
           result.title == title and \
           result.publication_year == publication_year:

            return

        self.assertFalse(True)

    def test_delete_book(self):
        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string())

        theme = Theme(description = random_string())

        created_theme_id = BookRepositoryTest.theme_repository.add(theme)
        created_book_id = BookRepositoryTest.book_repository.add(book, created_theme_id)

        BookRepositoryTest.book_repository.delete(created_book_id)

        result = BookRepositoryTest.book_repository.get_by_id(created_book_id)
        self.assertEqual(result, None)

class ReviewRepositoryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.theme_repository  = ThemeRepository(cls.conn)
        cls.book_repository   = BookRepository(cls.conn)
        cls.review_repository = ReviewRepository(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_review(self):
        theme = Theme(description = random_string())
        created_theme_id = ReviewRepositoryTest.theme_repository.add(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string() )
        created_book_id = ReviewRepositoryTest.book_repository.add(book, created_theme_id)

        guest = random_string()
        content = random_string()

        review = Review(guest = guest, content = content)
        ReviewRepositoryTest.review_repository.add(review, created_book_id)

        result = ReviewRepositoryTest.review_repository.get_all(created_book_id)

        for r in result:
            if r.guest == guest and \
               r.content == content:

                return

        self.assertFalse(True)

    def test_delete_review(self):
        theme = Theme(description = random_string())
        created_theme_id = ReviewRepositoryTest.theme_repository.add(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string() )
        created_book_id = ReviewRepositoryTest.book_repository.add(book, created_theme_id)

        guest = random_string()
        content = random_string()

        review = Review(guest = guest, content = content)
        created_review_id = ReviewRepositoryTest.review_repository.add(review, created_book_id)

        ReviewRepositoryTest.review_repository.delete(created_review_id)

        result = ReviewRepositoryTest.review_repository.get_by_id(created_review_id)

        self.assertEqual(result, None)

class ScoreRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("blog_unit_test.db")

        with open("src/schema.sql", "r") as schema:
            schema_script = schema.read()
            cls.conn.executescript(schema_script)

        cls.theme_repository = ThemeRepository(cls.conn)
        cls.book_repository  = BookRepository(cls.conn)
        cls.score_repository = ScoreRepository(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_create_score(self):
        theme = Theme(description = random_string())
        created_theme_id = ScoreRepositoryTest.theme_repository.add(theme)

        book = Book(author = random_string(),
                    title = random_string(),
                    publication_year = random_string() )
        created_book_id = ScoreRepositoryTest.book_repository.add(book, created_theme_id)

        guest = random_string()
        value = random.randint(1,5)

        score = Score(guest,value)
        score_id = ScoreRepositoryTest.score_repository.add(score, created_book_id)

        result = ScoreRepositoryTest.score_repository.get_all(created_book_id)
        for s in result:
            if s._id == score_id and s.value == value:
                return

        self.assertFalse(True)