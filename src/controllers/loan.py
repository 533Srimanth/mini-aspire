import json
from flask import Blueprint, request, jsonify

from models.loan import Loan, LoanRequest, LoansResponse, ApproveLoanResponse
from models.repayment import CustomerRepaymentRequest, CustomerRepaymentResponse
from models.user import User
from services.loan import LoanService
from services.user import UserService
from auth import token_required, admin_token_required
from config import Config


class LoanController(Blueprint):
    def __init__(self, loan_service: LoanService, user_service: UserService, app_config: Config):
        super(LoanController, self).__init__('loans', 'loans', url_prefix='/loans')
        self.loan_service = loan_service
        self.user_service = user_service
        self.app_config = app_config

        @self.route('/', methods=['POST'])
        def create():
            return json.dumps(self._create(headers=request.headers, loan_details=request.json), default=str)

        @self.route('/', methods=['GET'])
        def fetch_all():
            return jsonify(self._fetch_all(headers=request.headers))

        @self.route('/<id>', methods=['GET'])
        def fetch_by_id(id: str):
            return jsonify(self._fetch_by_id(headers=request.headers, id=id))

        @self.route('/<loan_id>/repay', methods=['POST'])
        def make_customer_repayment(loan_id: str):
            return jsonify(self._make_customer_repayment(headers=request.headers, loan_id=loan_id, repayment_details=request.json))

        @self.route('/<loan_id>/approve', methods=['PATCH'])
        def approve_loan(loan_id: str):
            return jsonify(self._approve_loan(headers=request.headers, loan_id=loan_id))

    @token_required
    def _create(self, user: User, loan_details: dict):
        loan_request = LoanRequest.from_dict(loan_details)
        loan = self.loan_service.create(loan_request, user)
        return loan.to_loan_response()

    @token_required
    def _fetch_by_id(self, user: User, id: str):
        loan = self.loan_service.fetch_by_id(id)
        assert loan.user.id == user.id
        return loan.to_loan_response()

    @token_required
    def _fetch_all(self, user: User):
        loans = self.loan_service.fetch_by_user_id(user.id)
        return LoansResponse(
            message = "Success",
            count = len(loans),
            loans = [x.to_loan_response() for x in loans]
        )

    @token_required
    def _make_customer_repayment(self, user:User, loan_id: str, repayment_details: dict):
        customer_repayment_request = CustomerRepaymentRequest.from_dict(repayment_details)
        loan = self.loan_service.fetch_by_id(loan_id)
        assert loan.user.id == user.id

        loan.consume_customer_repayment(customer_repayment_request)
        return CustomerRepaymentResponse(
            message = "Success",
            scheduled_repayments = loan.scheduled_repayments
        )

    @admin_token_required
    def _approve_loan(self, loan_id: str):
        self.loan_service.approve(loan_id)
        return ApproveLoanResponse(
            id = loan_id,
            message = "Loan successfully approved"
        )

