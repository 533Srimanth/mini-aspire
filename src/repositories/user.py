from typing import Protocol
from models.user import User


class UserRepository(Protocol):
    def create(self, user: User):
        ...

    def fetch_all(self):
        ...

    def fetch_by_id(self, id):
        ...
