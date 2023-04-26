import uuid

from flask import Blueprint, jsonify, request
from main import app, repository_container
from models.user import User

user_controller = Blueprint('users', 'users', url_prefix='/users')


@user_controller.route('/', methods=['POST'])
def create():
    user_json = request.json
    user_json['id'] = str(uuid.uuid4())
    user = User.from_dict(user_json)
    repository_container.user_repository.create(user)

    return jsonify(user.to_dict())


@user_controller.route('/', methods=['GET'])
def fetch_all():
    users = repository_container.user_repository.fetch_all()
    return jsonify(message="Success", count=len(users), users= [x.to_dict() for x in users])


@user_controller.route('/<id>', methods=['GET'])
def fetch(id):
    user = repository_container.user_repository.fetch_by_id(id)
    return jsonify(user.to_dict())
