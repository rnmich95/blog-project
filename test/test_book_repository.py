import sqlite3
import unittest

import schema
from model import Book, Topic
from test.util import random_string
from repository.book_repository import BookRepository
from repository.topic_repository import TopicRepository


class TestBookRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        con = sqlite3.connect("blog_unit_test.db")
        schema.init_db(con)
        cls.bookRepository = BookRepository(con)
        cls.topicRepository = TopicRepository(con)

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
        result = TestBookRepository.bookRepository.get_all()

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