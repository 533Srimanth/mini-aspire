from typing import Protocol
from models.loan import Loan, LoanStatus


class LoanRepository(Protocol):
    def create(self, loan: Loan):
        ...

    def fetch_by_id(self, id: str):
        ...

    def fetch_by_user_id(self, user_id: str):
        ...

    def update_loan_status(self, id: str, status: LoanStatus):
        ...
