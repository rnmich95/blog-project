from dataclasses import dataclass

@dataclass
class Theme:
    description: str

    @classmethod
    def from_json(cls, json):
        assert json["description"].strip() != "", "No description provided"
        return cls(
            description = json["description"] )

@dataclass
class PersistedTheme(Theme):
    _id: int

@dataclass
class Book:
    author: str
    title: str
    publication_year: str
    theme_id: int

    @classmethod
    def from_json(cls, json):
        assert json["author"].strip() != "", "No author provided"
        assert json["title"].strip() != "", "No title provided"
        assert json["publication_year"].strip() != "", "No publication year provided"
        assert json["theme_id"] != None, "No theme id provided"
        return cls(
            author = json["author"],
            title = json["title"],
            publication_year = json["publication_year"],
            theme_id = json["theme_id"] )

@dataclass
class PersistedBook(Book):
    _id: int

@dataclass
class Review:
    guest: str
    content: str
    book_id: int

@dataclass
class PersistedReview(Review):
    _id: int

@dataclass
class Score:
    guest: str
    value: int
    book_id: int

@dataclass
class PersistedScore(Score):
    _id: int