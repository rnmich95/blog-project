import logging
import traceback
from model import Book, Review, Score, Theme
from dataclasses import asdict
from jsonschema import validate
from flask import Blueprint, current_app, jsonify, request

""" Blueprint: a way to organize a group of related views and other code """
api = Blueprint('api', __name__)

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
            "publication_year": {"type": "string"},
            "theme_id": {"type": "number"}
        },
        "required": ["author", "title", "publication_year", "theme_id"],
        "additionalProperties": False,
    },

    Review.__name__: {
        "type": "object",
        "properties": {
           "guest": {"type": "string"},
           "content": {"type": "string"},
           "book_id": {"type": "number"}
        },
        "required": ["guest", "content", "book_id"],
        "additionalProperties": False,
    },

    Score.__name__: {
        "type": "object",
        "properties": {
            "guest": {"type": "string"},
            "value": {"type": "number"},
            "book_id": {"type": "number"}
        },
        "required": ["guest", "value", "book_id"],
        "additionalProperties": False,
    }
}

def validate_and_build(cls, data):
    validate(instance=data, schema=SCHEMAS[cls.__name__])
    return cls.from_json(data)

@api.route('/themes', methods=['GET'])
def get_themes():
    service = current_app.config["services"]["theme"]
    themes = service.get_all_themes()

    dics = [t.to_dict() for t in themes]

    return jsonify(dics)

@api.route('/themes', methods=['POST'])
def create_theme():
    try:
        theme = validate_and_build(Theme, request.json)

        service = current_app.config["services"]["theme"]
        _id = service.add_theme(theme)

        return jsonify({"created_id" : _id}), 201

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 406

@api.route('/books/<int:theme_id>', methods=['GET'])
def get_books(theme_id):
    service = current_app.config['services']['book']
    books = service.get_all_books(theme_id)
    dics = [b.to_dict() for b in books]

    return jsonify(dics)

@api.route('/books/<int:theme_id>', methods=['POST'])
def create_book(theme_id):
    try:
        book = validate_and_build(Book, request.json)

        service = current_app.config["services"]["book"]
        _id = service.add_book(book)

        return jsonify({"created_id" : _id}), 201

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 406

@api.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = validate_and_build(Book, request.json)

        service = current_app.config["services"]["book"]
        persisted_book = service.get_one_book(book_id)

        if persisted_book:
            service.update_book(book, book_id)
            return jsonify({"persisted_id" : book_id}), 200
        return jsonify({"error": "Book not found"}), 404

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 406

@api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    service = current_app.config["services"]["book"]

    persisted_book = service.get_one_book(book_id)
    if persisted_book:
        service.delete_book(book_id)

        return jsonify({"deleted_id" : book_id}), 200

    return jsonify({"error": "Book not found"}), 404

@api.route('/reviews/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    service = current_app.config['services']['review']
    reviews = service.get_all_reviews(book_id)
    dics = [r.to_dict() for r in reviews]

    return jsonify(dics)

@api.route('/reviews/<int:book_id>', methods=['POST'])
def create_review(book_id):
    try:
        review = validate_and_build(Review, request.json)

        service = current_app.config["services"]["review"]
        _id = service.add_review(review)

        return jsonify({"created_id" : _id}), 201

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 406

@api.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    service = current_app.config["services"]["review"]

    persisted_review = service.get_one_review(review_id)
    if persisted_review:
        service.delete_review(review_id)

        return jsonify({"deleted_id" : review_id}), 200

    return jsonify({"error": "Review not found"}), 404

@api.route('/overall_score/<int:book_id>', methods=['GET'])
def get_average_score(book_id):
    service = current_app.config['services']['score']
    score = service.get_avarage_score(book_id)

    return jsonify({"overall_score" : score})

@api.route('/scores/<int:book_id>', methods=['POST'])
def add_score(book_id):
    try:
        score = validate_and_build(Score, request.json)

        service = current_app.config["services"]["score"]
        _id = service.add_score(score)

        return jsonify({"created_id" : _id}), 201

    except Exception as e:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 406