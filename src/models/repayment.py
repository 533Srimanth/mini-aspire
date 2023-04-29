from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum


class ScheduledRepaymentStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"


@dataclass
class ScheduledRepayment:
    amount: int
    paid: int
    balance: int
    due_date: datetime
    status: ScheduledRepaymentStatus

    def consume_payment(self, amount: int):
        self.paid += min(amount, self.balance)
        if self.paid == self.amount:
            self.status = ScheduledRepaymentStatus.PAID

        temp = self.balance
        self.balance -= min(self.balance, amount)
        amount -= min(amount, temp)

        return amount

    def is_paid(self):
        return self.status == ScheduledRepaymentStatus.PAID

    def __eq__(self, other):
        return self.amount == other.amount and self.due_date == other.due_date and self.status == other.status and self.paid == other.paid and self.balance == other.balance


@dataclass
class CustomerRepayment:
    amount: int
    currency: str
    issue_date: datetime


@dataclass_json
@dataclass
class CustomerRepaymentRequest:
    amount: int
    currency: str


@dataclass
class CustomerRepaymentResponse:
    message: str
    scheduled_repayments: list[ScheduledRepayment]
