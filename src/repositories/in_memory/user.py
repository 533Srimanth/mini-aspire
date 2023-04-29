from repositories.user import UserRepository
from models.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.store = {}
        self.token_store = {}

    def create(self, user: User):
        self.store[user.id] = user

    def fetch_all(self):
        return self.store.values()

    def fetch_by_id(self, id: str):
        return self.store[id]

    def fetch_by_credentials(self, email: str, password_hash: str):
        return next(user for id, user in self.store.items() if user.email == email and user.password_hash == password_hash)

    def store_token(self, user: User, token: str):
        self.token_store[token] = user

    def fetch_by_token(self, token: str):
        return self.token_store[token]
