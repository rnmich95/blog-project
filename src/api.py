from model import Book, Theme
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
    }
}

def validate_and_build(cls, data):
    validate(instance=data, schema=SCHEMAS[cls.__name__])
    return cls.from_json(data)

@api.route('/themes', methods=['GET'])
def get_themes():
    service = current_app.config["services"]["theme"]
    themes = service.get_all_themes()
    """ * mapear explicitamente com uma funcao ou classe * """
    dics = [asdict(t) for t in themes]

    return jsonify(dics)
"""
arquivo view

@app.route('/themes/new', methods=['GET'])
def show_theme_form():
    return render_template("create_theme.html")
"""

@api.route('/themes', methods=['POST'])
def create_theme():
    """ estou engolindo o erro
        inserir o stack trace completo e timestamp dentro de um arquivo e
        imprima o erro
    """
    try:
        theme = validate_and_build(Theme, request.json)
    except:
        return jsonify({"error": "Json format not acceptable"}), 406

    service = current_app.config["services"]["theme"]
    _id = service.add_theme(theme)

    return jsonify({"created_id" : _id}), 201

@api.route('/books/<int:theme_id>', methods=['GET'])
def get_books(theme_id):
    service = current_app.config['services']['book']
    books = service.get_all_books(theme_id)
    dics = [asdict(b) for b in books]

    return jsonify(dics)

@api.route('/books/<int:theme_id>', methods=['POST'])
def create_book(theme_id):
    try:
        book = validate_and_build(Book, request.json)
    except:
        return jsonify({"error": "Json format not acceptable"}), 406

    service = current_app.config["services"]["book"]
    _id = service.add_book(book)

    return jsonify({"created_id" : _id}), 201

@api.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = validate_and_build(Book, request.json)
    except:
        return jsonify({"error": "Json format not acceptable"}), 406

    service = current_app.config["services"]["book"]

    persisted_book = service.get_one_book(book_id)
    if persisted_book:
        service.update_book(book, book_id)

        return jsonify({"persisted_id" : book_id}), 200

    return jsonify({"error": "Book not found"}), 404

@api.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    service = current_app.config["services"]["book"]

    persisted_book = service.get_one_book(book_id)
    if persisted_book:
        service.delete_book(book_id)

        return jsonify({"deleted_id" : book_id}), 200

    return jsonify({"error": "Book not found"}), 404