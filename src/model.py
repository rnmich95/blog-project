from dataclasses import dataclass

@dataclass
class Topic:
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
    publication_date: str

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