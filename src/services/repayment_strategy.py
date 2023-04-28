import datetime
from typing import Protocol

from models.repayment import ScheduledRepayment, ScheduledRepaymentStatus
from models.loan import Loan


class RepaymentStrategyFactory:
    @staticmethod
    def build(name: str):
        if name == "WEEKLY":
            return WeeklyRepaymentStrategy()


class RepaymentStrategy(Protocol):
    def generate_repayments(self, loan: Loan) -> list[ScheduledRepayment]:
        ...


class WeeklyRepaymentStrategy(RepaymentStrategy):
    def __init__(self):
        ...

    def generate_repayments(self, loan: Loan) -> list[ScheduledRepayment]:
        repayments = []

        repayment_date = loan.request_date
        for i in range(loan.term):
            repayment_date += datetime.timedelta(days=7)
            amount_per_repayment = loan.amount//loan.term + (loan.amount % loan.term if i == loan.term - 1 else 0)
            repayment = ScheduledRepayment(
                amount = amount_per_repayment,
                balance = amount_per_repayment,
                paid = 0,
                due_date = repayment_date,
                status = ScheduledRepaymentStatus.PENDING
            )
            repayments.append(repayment)

        return repayments

