import logging
import traceback
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
import requests

from model import Book, Review

view = Blueprint('view', __name__)

@view.route('/base', methods=['GET'])
def show_base_template():
    return render_template('base.html')

@view.route('/', methods=['GET'])
def show_list_of_themes():

    service = current_app.config['services']['theme']
    themes = service.get_all_themes()

    return render_template('theme/list.html', themes = themes)

@view.route('/add_theme', methods=['GET'])
def show_create_theme_form():
    return render_template('theme/create.html')

@view.route('/list_books/<int:theme_id>', methods=['GET'])
def show_list_of_books(theme_id):

    service = current_app.config['services']['book']
    books = service.get_all_books(theme_id)

    return render_template('book/list.html', books = books, t_id = theme_id)

@view.route('/add_book/<int:theme_id>', methods=['GET'])
def show_create_book_form(theme_id):
    return render_template('book/create.html', t_id = theme_id)

@view.route('/process_book_form', methods=['POST'])
def process_book_form_fields():

    author = request.form['author']
    title  = request.form['title']
    year   = request.form['year']
    _id    = request.form['theme_id']

    # validation

    book = Book(author = author,
                title = title,
                publication_year = year,
                theme_id = _id)

    try:
        service = current_app.config['services']['book']
        service.add_book(book)

        books = service.get_all_books(_id)

        return render_template('book/list.html', books = books, t_id = _id)

    except Exception as e:

        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

@view.route('/list_reviews/<int:book_id>', methods=['GET'])
def show_list_of_reviews(book_id):

    service = current_app.config['services']['review']
    reviews = service.get_all_reviews(book_id)

    return render_template('review/list.html', reviews = reviews, b_id = book_id)

@view.route('/add_review/<int:book_id>', methods=['GET'])
def show_create_review_form(book_id):
    return render_template('review/create.html', b_id = book_id)

@view.route('/process_review_form', methods=['POST'])
def process_review_form_fields():

    guest = request.form['guest']
    content = request.form['content']
    _id = request.form['book_id']

    # validation

    review = Review(guest = guest, content = content, book_id = _id)

    try:
        service = current_app.config['services']['review']
        service.add_review(review)

        reviews = service.get_all_reviews(_id)

        return render_template('review/list.html', reviews = reviews, b_id = _id)

    except Exception as e:

        logging.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 400