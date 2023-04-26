from dataclasses import dataclass
from user import User
from repayment import Repayment

class LoanStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFAULTED = "defaulted"

@dataclass
class Loan:
    user: User
    repayments: List[Repayment]
    status: LoanStatus