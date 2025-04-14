from dataclasses import dataclass


@dataclass
class Topic:
    description: str


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
class Rate:
    guest: str
    value: int