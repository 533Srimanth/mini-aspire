from repositories.user import UserRepository
from models.user import User
import uuid


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.store = {}

    def create(self, user: User):
        self.store[user.id] = user
        print(self.store)

    def fetch_all(self):
        return self.store.values()

    def fetch_by_id(self, id):
        return self.store[id]
