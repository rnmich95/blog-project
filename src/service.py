from model import Book, Review, Score, Topic
from repository import BookRepository, ReviewRepository, ScoreRepository, TopicRepository


class TopicService:
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def get_all_topics(self):
        return self.topic_repository.get_all()

    def add_topic(self, topic: Topic):
        return self.topic_repository.add(topic)

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get_all_books(self, topic_id):
        return self.book_repository.get_all(topic_id)

    def add_book(self, book: Book, topic_id):
        return self.book_repository.add(book, topic_id)

    def update_book(self, book: Book, book_id):
        return self.book_repository.update(book, book_id)

    def delete_book(self, book_id):
        return self.book_repository.delete(book_id)

class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def get_all_reviews(self, book_id):
        return self.review_repository.get_all(book_id)

    def add_review(self, review: Review, book_id):
        return self.review_repository.add(review, book_id)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

class ScoreService:
    def __init__(self, score_repository: ScoreRepository):
        self.score_repository = score_repository

    def get_avarage_score(self, book_id):
        scores  = self.score_repository.get_all(book_id)
        values  = [s.value for s in scores]
        avarage = sum(values) / len(values)

        return avarage

    def add_score(self, score: Score, book_id):
        return self.score_repository.add(score, book_id)