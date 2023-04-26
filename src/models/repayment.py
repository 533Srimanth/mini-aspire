from dataclasses import dataclass
from datetime import datetime

class RepaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"

@dataclass
class Repayment:
    due_date: datetime
    amount: int
    currency: str
    status: RepaymentStatus
