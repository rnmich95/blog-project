from dataclasses import asdict
import sqlite3
import sys
import logging

from typing import Dict
from flask import Flask, current_app, jsonify, request
from jsonschema import validate

from config import read_config
from model import Book, Theme
from repository import BookRepository, ReviewRepository, ScoreRepository, ThemeRepository
from service import BookService, ReviewService, ScoreService, ThemeService

logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

SCHEMAS = {
    Theme.__name__: {
        "type": "object",
        "properties": {
            "description": {"type": "string"}
        },
        "required" : ["description"],
        "additionalProperties": False,
    },

    Book.__name__: {
        "type": "object",
        "properties": {
            "author": {"type": "string"},
            "title": {"type": "string"},
            "publication_year": {"type": "string"}
        },
        "required": ["author", "title", "publication_year"],
        "additionalProperties": False,
    }
}

def validate_and_build(cls, data):
    validate(instance=data, schema=SCHEMAS[cls.__name__])
    return cls.from_json(data)

@app.route('/themes', methods=['GET'])
def get_themes():
    service = current_app.config["services"]["theme"]
    themes = service.get_all_themes()
    dics = [asdict(t) for t in themes]

    return jsonify(dics)

@app.route('/themes', methods=['POST'])
def create_theme():
    try:
        theme = validate_and_build(Theme, request.json)
    except:
        return jsonify({"error": "Json format not acceptable"}), 406

    service = current_app.config["services"]["theme"]
    _id = service.add_theme(theme)

    return jsonify({"created_id" : _id}), 201

@app.route('/books/<int:theme_id>', methods=['GET'])
def get_books(theme_id):
    service = current_app.config['services']['book']
    books = service.get_all_books(theme_id)
    dics = [asdict(b) for b in books]

    return jsonify(dics)

def init_repositories(con) -> Dict[str,object]:
    return {
        "theme" : ThemeRepository(con),
        "book" : BookRepository(con),
        "review" : ReviewRepository(con),
        "score": ScoreRepository(con)
    }

def init_services(repositories) -> Dict[str,object]:
    return {
        "theme" : ThemeService(repositories["theme"]),
        "book" : BookService(repositories["book"]),
        "review" : ReviewService(repositories["review"]),
        "score" : ScoreService(repositories["score"])
    }

if __name__ == '__main__':

    config = read_config()

    conn = sqlite3.connect(sys.argv[1], check_same_thread=False)

    respositories = init_repositories(conn)

    services = init_services(respositories)

    app.config["services"] = services

    app.run(host=config.host, port=config.port, debug=config.debug)