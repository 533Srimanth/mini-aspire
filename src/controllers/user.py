from flask import Blueprint, jsonify, request

from models.user import User, UserSignUpRequest, UserLoginRequest, UserLoginResponse, UsersResponse
from services.user import UserService
from auth import admin_token_required, token_required
from config import Config
from exceptions import AuthorizationError


class UserController(Blueprint):
    def __init__(self, user_service: UserService, config: Config):
        super(UserController, self).__init__('users', 'users', url_prefix='/users')
        self.user_service = user_service
        self.app_config = config

        @self.route('/', methods=['POST'])
        def signup():
            return jsonify(self._signup(request.json))

        @self.route('/login', methods=['POST'])
        def login():
            return jsonify(self._login(request.json))

        @self.route('/', methods=['GET'])
        def fetch_all():
            return jsonify(self._fetch_all(headers=request.headers))

        @self.route('/<id>', methods=['GET'])
        def fetch(id):
            return jsonify(self._fetch(headers=request.headers, id=id))

    def _signup(self, user_details: dict):
        user_sign_up_request = UserSignUpRequest.from_dict(user_details)
        user = self.user_service.create(user_sign_up_request)
        return user.to_user_response()

    def _login(self, credentials):
        user_login_request = UserLoginRequest.from_dict(credentials)
        user, token = self.user_service.login(user_login_request)
        return UserLoginResponse(
            token = token,
            message = "Success",
            user = user.to_user_response()
        )

    @admin_token_required
    def _fetch_all(self):
        users = self.user_service.fetch_all()
        return UsersResponse(message="Success", count=len(users), users=[x.to_user_response() for x in users])

    @token_required
    def _fetch(self, user: User, id: str):
        if id != user.id:
            raise AuthorizationError()

        user = self.user_service.fetch_by_id(id)
        return user.to_user_response()
