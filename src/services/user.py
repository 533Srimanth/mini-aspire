import uuid

from repositories.user import UserRepository
from models.user import User, UserSignUpRequest, UserLoginRequest
from exceptions import EntityDoesNotExistException


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, details: UserSignUpRequest):
        user = User(
            id = str(uuid.uuid4()),
            name = details.name,
            email = details.email,
            password_hash = self.__generate_password_hash(details.password),
        )

        self.repository.create(user)
        return user

    def login(self, details: UserLoginRequest):
        try:
            user = self.repository.fetch_by_credentials(details.email, self.__generate_password_hash(details.password))
            token = str(uuid.uuid4())
            self.repository.store_token(user, token)
            return user, token
        except StopIteration:
            raise EntityDoesNotExistException("User")

    def fetch_all(self):
        return self.repository.fetch_all()

    def fetch_by_id(self, id: str):
        try:
            return self.repository.fetch_by_id(id)
        except KeyError:
            ids = object()
            ids.id = id
            raise EntityDoesNotExistException("User", ids)

    def fetch_by_token(self, token: str):
        return self.repository.fetch_by_token(token)

    @classmethod
    def __generate_password_hash(cls, password: str):
        return hash(password)
