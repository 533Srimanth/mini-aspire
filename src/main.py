import os

from flask import Flask

from repositories import factory
from config import Config

app = Flask("mini-aspire")
config = Config.load(os.getenv("CONFIG_FILE"))
repository_container = factory.RepositoryContainer(config.db)

from controllers.user import user_controller
app.register_blueprint(user_controller)

