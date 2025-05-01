import argparse
import sys
import logging
import sqlite3
from api import api
from view import view
from flask import Flask
from typing import Dict
from config import read_config
from repository import BookRepository, ReviewRepository, ScoreRepository, ThemeRepository
from service import BookService, ReviewService, ScoreService, ThemeService

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

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

    parser = argparse.ArgumentParser(description = "")

    parser.add_argument('db_file', help='select your SQLite .db file')

    args = parser.parse_args()

    config = read_config()

    # conn = sqlite3.connect(sys.argv[1], check_same_thread=False)

    conn = sqlite3.connect(args.db_file, check_same_thread=False)

    respositories = init_repositories(conn)

    services = init_services(respositories)

    app.config["services"] = services

    app.register_blueprint(api)

    app.register_blueprint(view)

    app.run(host=config.host, port=config.port, debug=config.debug)