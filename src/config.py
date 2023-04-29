import os

from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class Config:
    db: str
    admin_token: str
    repayment_strategy: str

    @staticmethod
    def load(file_path):
        if not file_path or not os.path.exists(file_path):
            config = Config(
                db = os.getenv('DB', 'IN-MEMORY'),
                admin_token = os.getenv('ADMIN_TOKEN', 'admin-token'),
                repayment_strategy = os.getenv('REPAYMENT_STRATEGY', 'WEEKLY'),
            )
            return config

        with open(file_path, 'r') as f:
            return Config.from_json(f.read())