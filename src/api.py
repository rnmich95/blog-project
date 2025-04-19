from dataclasses import asdict
import sqlite3
import sys
import logging

from typing import Dict
from flask import Flask, current_app, jsonify, request
from jsonschema import validate

from config import read_config
from model import Topic
from repository import BookRepository, ReviewRepository, ScoreRepository, TopicRepository
from service import BookService, ReviewService, ScoreService, TopicService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# topics = {}

SCHEMAS = {
    Topic.__name__: {
        "type": "object",
        "properties": {
            "description": {"type": "string"}
        },
        "required" : ["description"],
        "additionalProperties": False,
    }
}

def validate_and_build(cls, data):
    validate(instance=data, schema=SCHEMAS[cls.__name__])
    return cls.from_json(data)

@app.route('/topics', methods=['GET'])
def get_topics():

    service = current_app.config["services"]["topic"]
    topics = service.get_all_topics()
    dics = [asdict(t) for t in topics]

    return jsonify(dics)

@app.route('/topics', methods=['POST'])
def create_topic():
    try:
        topic = validate_and_build(Topic, request.json)
    except:
        return jsonify({"error": "Json format not acceptable"}), 406

    service = current_app.config["services"]["topic"]
    _id = service.add_topic(topic)

    return jsonify({"lastrowid" : _id}), 201


def init_repositories(con) -> Dict[str,object]:
    return {
        "topic" : TopicRepository(con),
        "book" : BookRepository(con),
        "review" : ReviewRepository(con),
        "score": ScoreRepository(con)
    }

def init_services(repositories) -> Dict[str,object]:
    return {
        "topic" : TopicService(repositories["topic"]),
        "book" : BookService(repositories["book"]),
        "review" : ReviewService(repositories["review"]),
        "score" : ScoreService(repositories["score"])
    }

if __name__ == '__main__':

    config = read_config()

    con = sqlite3.connect(sys.argv[1], check_same_thread=False)

    respositories = init_repositories(con)

    services = init_services(respositories)

    app.config["services"] = services

    app.run(host=config.host, port=config.port, debug=config.debug)