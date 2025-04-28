from model import Book, Review, Score, Theme
from repository import BookRepository, ReviewRepository, ScoreRepository, ThemeRepository

class ThemeService:
    def __init__(self, theme_repository: ThemeRepository):
        self.theme_repository = theme_repository

    def get_all_themes(self):
        return self.theme_repository.get_all()

    def add_theme(self, theme: Theme):
        return self.theme_repository.add(theme)

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get_all_books(self, theme_id):
        return self.book_repository.get_all(theme_id)

    def get_one_book(self, book_id):
        return self.book_repository.get_by_id(book_id)

    def add_book(self, book: Book):
        return self.book_repository.add(book)

    def update_book(self, book: Book, book_id):
        return self.book_repository.update(book, book_id)

    def delete_book(self, book_id):
        return self.book_repository.delete(book_id)

class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def get_all_reviews(self, book_id):
        return self.review_repository.get_all(book_id)

    def add_review(self, review: Review):
        return self.review_repository.add(review)

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

    def add_score(self, score: Score):
        return self.score_repository.add(score)