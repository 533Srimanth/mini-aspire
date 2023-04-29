from repositories.loan import LoanRepository
from models.loan import Loan, LoanStatus


class InMemoryLoanRepository(LoanRepository):
    def __init__(self):
        self.store = {}

    def create(self, loan: Loan):
        self.store[loan.id] = loan

    def fetch_by_user_id(self, user_id: str):
        return list(sorted(filter(lambda loan: loan.user.id == user_id, self.store.values()), key=lambda loan: loan.request_date, reverse = True))

    def fetch_by_id(self, id: str):
        return self.store[id]

    def update_loan_status(self, id: str, status: LoanStatus):
        self.store[id].status = status
