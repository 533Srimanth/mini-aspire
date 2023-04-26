import os

from dataclasses_json import dataclass_json
from dataclasses import dataclass

@dataclass_json
@dataclass
class Config:
    db: str

    @staticmethod
    def load(file_path):
        if not file_path or not os._exists(file_path):
            config = Config(db = os.getenv('DB', 'IN-MEMORY'))
            return config

        with open(file_path, 'r') as f:
            return Config.from_json(f.read())