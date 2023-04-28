import uuid
from datetime import datetime

from repositories.loan import LoanRepository
from models.loan import Loan, LoanStatus, LoanRequest
from models.user import User
from services.repayment_strategy import RepaymentStrategy
from exceptions import EntityDoesNotExistException


class LoanService:
    def __init__(self, repository: LoanRepository, repayment_strategy: RepaymentStrategy):
        self.repository = repository
        self.repayment_strategy = repayment_strategy

    def create(self, details: LoanRequest, user: User):
        loan = Loan(
            id = str(uuid.uuid4()),
            amount = details.amount,
            currency = details.currency,
            term = details.term,
            user = user,
            status = LoanStatus.PENDING,
            request_date = datetime.now(),
            scheduled_repayments = [],
            customer_repayments = []
        )
        loan.scheduled_repayments = self.repayment_strategy.generate_repayments(loan)

        self.repository.create(loan)
        return loan

    def fetch_by_user_id(self, user_id: str):
        return self.repository.fetch_by_user_id(user_id)

    def fetch_by_id(self, id: str):
        try:
            return self.repository.fetch_by_id(id)
        except KeyError:
            ids = object()
            ids.id = id
            raise EntityDoesNotExistException("Loan", ids)

    def approve(self, id: str):
        return self.repository.update_loan_status(id, LoanStatus.APPROVED)
