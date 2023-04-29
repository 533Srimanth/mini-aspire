import tempfile
import json

from config import Config


def test_load_config_from_file():
    config = Config(
        db = 'MYSQL',
        admin_token = 'ADMIN_TEST_TOKEN',
        repayment_strategy = 'MONTHLY'
    )

    with tempfile.NamedTemporaryFile() as f:
        with open(f.name, 'w') as f1:
            json.dump({
                'db': 'MYSQL',
                'admin_token': 'ADMIN_TEST_TOKEN',
                'repayment_strategy': 'MONTHLY'
            }, f1)
        loaded_config = Config.load(f.name)
        assert config == loaded_config

