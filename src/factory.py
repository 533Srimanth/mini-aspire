import os
from flask import Flask

from controllers.user import UserController
from controllers.loan import LoanController
from services.user import UserService
from services.loan import LoanService
from repositories.user import UserRepository
from repositories.loan import LoanRepository
from repositories.factory import RepositoryFactory
from services.repayment_strategy import RepaymentStrategy, RepaymentStrategyFactory
from config import Config


dependency_graph = {
    'app': ['user_controller', 'loan_controller'],
    'user_controller': ['user_service', 'config'],
    'loan_controller': ['loan_service', 'user_service', 'config'],
    'user_service': ['user_repository'],
    'loan_service': ['loan_repository', 'repayment_strategy'],
    'user_repository': ['config'],
    'loan_repository': ['config'],
    'repayment_strategy': ['config'],
    'config': []
}


def initialize_one(arg):
    return initialize(arg)[arg]


def initialize(*args):
    def initialize_core(*args, initialized_entities):
        entities = {}
        for arg in args:
            if arg not in initialized_entities:
                entities[arg] = initializer_methods[arg](**initialize_core(*dependency_graph[arg], initialized_entities=initialized_entities))
                initialized_entities[arg] = entities[arg]
            else:
                entities[arg] = initialized_entities[arg]
        return entities

    return initialize_core(*args, initialized_entities={})


def app(user_controller: UserController, loan_controller: LoanController):
    app = Flask("mini-aspire")
    app.register_blueprint(user_controller)
    app.register_blueprint(loan_controller)

    return app


def user_controller(user_service: UserService, config: Config):
    return UserController(user_service, config)


def loan_controller(loan_service: LoanService, user_service: UserService, config: Config):
    return LoanController(loan_service, user_service, config)


def user_service(user_repository: UserRepository):
    return UserService(user_repository)


def loan_service(loan_repository: LoanRepository, repayment_strategy: RepaymentStrategy):
    return LoanService(loan_repository, repayment_strategy)


def user_repository(config: Config):
    return RepositoryFactory.build_user_repository(config.db)


def loan_repository(config: Config):
    return RepositoryFactory.build_loan_repository(config.db)


def repayment_strategy(config: Config):
    return RepaymentStrategyFactory.build(config.repayment_strategy)


def config():
    return Config.load(os.getenv("CONFIG_FILE"))


initializer_methods = {
    'app': app,
    'user_controller': user_controller,
    'loan_controller': loan_controller,
    'user_service': user_service,
    'loan_service': loan_service,
    'user_repository': user_repository,
    'loan_repository': loan_repository,
    'repayment_strategy': repayment_strategy,
    'config': config
}
