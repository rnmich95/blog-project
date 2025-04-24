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
class Book:
    author: str
    title: str
    publication_year: str

    @classmethod
    def from_json(cls, json):
        assert json["author"].strip() != "", "No author provided"
        assert json["title"].strip() != "", "No title provided"
        assert json["publication_year"].strip() != "", "No publication year provided"
        return cls(
            author = json["author"],
            title = json["title"],
            publication_year = json["publication_year"] )

@dataclass
class PersistedBook(Book):
    theme_id: int

@dataclass
class Review:
    guest: str
    content: str

@dataclass
class Score:
    guest: str
    value: int

@dataclass
class PersistedScore:
    _id: int
    value: int