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

    def to_dict(self):
     return {"id": self._id,
             "description": self.description }

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

    def to_dict(self):
        return {"id": self._id,
                "author": self.author,
                "title": self.title,
                "publication_year": self.publication_year,
                "theme_id": self.theme_id}

@dataclass
class Review:
    guest: str
    content: str
    book_id: int

    @classmethod
    def from_json(cls, json):
        assert json["guest"].strip() != "", "No guest provided"
        assert json["content"].strip() != "", "No content provided"
        assert json["book_id"] != None, "No book_id provided"
        return cls(
            guest = json["guest"],
            content = json["content"],
            book_id = json["book_id"] )

@dataclass
class PersistedReview(Review):
    _id: int

    def to_dict(self):
        return {"id": self._id,
                "guest": self.guest,
                "content": self.content,
                "book_id": self.book_id}

@dataclass
class Score:
    guest: str
    value: int
    book_id: int

    @classmethod
    def from_json(cls, json):
        assert json["guest"].strip() != "", "No guest provided"
        assert json["value"] != None, "No value provided"
        assert json["book_id"] != None, "No book_id provided"
        return cls(
            guest = json["guest"],
            value = json["value"],
            book_id = json["book_id"] )

@dataclass
class PersistedScore(Score):
    _id: int

    def to_dict(self):
        return {"_id": self._id,
                "guest": self.guest,
                "value": self.value,
                "book_id": self.book_id}