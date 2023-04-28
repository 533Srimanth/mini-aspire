from repositories.in_memory.user import InMemoryUserRepository
from repositories.in_memory.loan import InMemoryLoanRepository


class RepositoryFactory:
    @staticmethod
    def build_user_repository(db):
        if db == 'IN-MEMORY':
            return InMemoryUserRepository()

    @staticmethod
    def build_loan_repository(db):
        if db == 'IN-MEMORY':
            return InMemoryLoanRepository()


