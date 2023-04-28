import time
from enum import Enum
from datetime import datetime

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from models.user import User, UserResponse
from models.repayment import ScheduledRepayment, CustomerRepayment, CustomerRepaymentRequest
from currency import currency_exchange_value


class LoanStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PAID = "PAID"


@dataclass
class Loan:
    id: str
    amount: int
    currency: str
    term: int
    user: User
    scheduled_repayments: list[ScheduledRepayment]
    customer_repayments: list[CustomerRepayment]
    status: LoanStatus
    request_date: datetime

    def to_loan_response(self):
        return LoanResponse(
            id = self.id,
            amount = self.amount,
            currency = self.currency,
            term = self.term,
            user = self.user.to_user_response(),
            scheduled_repayments = self.scheduled_repayments,
            customer_repayments = self.customer_repayments,
            status = self.status,
            request_date = self.request_date
        )

    def consume_customer_repayment(self, request: CustomerRepaymentRequest):
        self.customer_repayments.append(CustomerRepayment(
            amount = request.amount,
            currency = request.currency,
            issue_date = datetime.now()
        ))

        scheduled_repayment_index = 0
        balance = currency_exchange_value(request.currency, request.amount, self.currency)
        while balance > 0 and scheduled_repayment_index < len(self.scheduled_repayments):
            scheduled_repayment = self.scheduled_repayments[scheduled_repayment_index]
            balance = scheduled_repayment.consume_payment(balance)
            scheduled_repayment_index += 1

        if self.scheduled_repayments[-1].is_paid():
            self.status = LoanStatus.PAID


@dataclass_json
@dataclass
class LoanRequest:
    amount: int
    currency: str
    term: int


@dataclass
class LoanResponse:
    id: str
    amount: int
    currency: str
    term: int
    user: UserResponse
    scheduled_repayments: list[ScheduledRepayment]
    customer_repayments: list[CustomerRepayment]
    status: LoanStatus
    request_date: datetime


@dataclass
class LoansResponse:
    message: str
    count: int
    loans: list[LoanResponse]


@dataclass
class ApproveLoanResponse:
    id: str
    message: str
