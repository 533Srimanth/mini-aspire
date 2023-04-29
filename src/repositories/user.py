from typing import Protocol
from models.user import User


class UserRepository(Protocol):
    def create(self, user: User):
        ...

    def fetch_all(self):
        ...

    def fetch_by_id(self, id: str):
        ...

    def fetch_by_credentials(self, email: str, password_hash: str):
        ...

    def store_token(self, user: User, token: str):
        ...

    def fetch_by_token(self, token: str):
        ...
