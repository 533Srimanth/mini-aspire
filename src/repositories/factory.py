from .in_memory.user import InMemoryUserRepository


class RepositoryContainer:
    def __init__(self, db: str):
        self.user_repository = self.__create_user_repository(db)

    @staticmethod
    def __create_user_repository(db):
        if db == 'IN-MEMORY':
            return InMemoryUserRepository()


