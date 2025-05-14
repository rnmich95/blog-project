import argparse
import os
import sys
import logging
import sqlite3
from api import api
from view import view
from flask import Flask, json
from typing import Dict
from config import read_config
from repository import BookRepository, ReviewRepository, ScoreRepository, ThemeRepository
from service import BookService, ReviewService, ScoreService, ThemeService

logging.basicConfig(
    filename='app.log',
    # detailed information, typically only of interest to a developer trying to diagnose a problem
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(lineno)d - %(message)s'
)

app = Flask(__name__)

def init_db(db_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.dirname(current_dir)

    settings_path = os.path.join(project_root, "settings.json")

    with open(settings_path, "r") as s:
         settings = json.load(s)

    schema_path = os.path.join(project_root, settings["schema_path"])

    conn = sqlite3.connect(args.db_file, check_same_thread=False)

    with open(schema_path, "r") as schema:
            schema_script = schema.read()
            conn.executescript(schema_script)

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
    parser.add_argument('--init-db', action='store_true', help='initialize empty .db file')

    args = parser.parse_args()

    config = read_config()

    if args.init_db:
         init_db(args.db_file)

    if not os.path.exists(args.db_file):
         print("Attention, the selected file does not exist. Type --init-db to define an empty .db file.")
         exit(1)

    conn = sqlite3.connect(args.db_file, check_same_thread=False)

    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.dirname(current_dir)

    settings_path = os.path.join(project_root, "settings.json")

    with open(settings_path, "r") as s:
         settings = json.load(s)

    schema_path = os.path.join(project_root, settings["schema_path"])

    with open(schema_path, "r") as schema:
            schema_script = schema.read()
            conn.executescript(schema_script)
    """

    respositories = init_repositories(conn)

    services = init_services(respositories)

    app.config["services"] = services

    app.register_blueprint(api)

    app.register_blueprint(view)

    app.run(host=config.host, port=config.port, debug=config.debug)