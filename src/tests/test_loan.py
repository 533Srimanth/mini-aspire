import pytest
import datetime

from models.loan import LoanStatus
from models.repayment import ScheduledRepayment, ScheduledRepaymentStatus
from factory import initialize
from exceptions import AuthorizationError, AuthFailedException, AuthHeaderMissingException, EntityDoesNotExistException


def dummy_user():
    return {
        "name": "Srimanth",
        "email": "533srimanth@gmail.com",
        "password": "password"
    }


def dummy_loan(amount, currency, term):
    return {
        "amount": amount,
        "currency": currency,
        "term": term
    }


@pytest.fixture
def auth_token_and_loan_controller():
    controllers = initialize('user_controller', 'loan_controller')

    user_controller = controllers['user_controller']
    user_controller._signup(dummy_user())
    login_response = user_controller._login(dummy_user())
    loan_controller = controllers['loan_controller']

    return login_response.token, loan_controller


@pytest.fixture
def auth_token_and_controllers():
    controllers = initialize('user_controller', 'loan_controller')

    user_controller = controllers['user_controller']
    user_controller._signup(dummy_user())
    login_response = user_controller._login(dummy_user())
    loan_controller = controllers['loan_controller']

    return login_response.token, loan_controller, user_controller


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_create_loan(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    assert loan.status == LoanStatus.PENDING
    assert loan.currency == loan_details['currency']
    assert loan.term == loan_details['term']
    assert loan.amount == loan_details['amount']
    assert len(loan.scheduled_repayments) == loan.term

    repayment_date = loan.request_date
    for repayment in loan.scheduled_repayments[:-1]:
        repayment_date += datetime.timedelta(days=7)
        assert repayment == ScheduledRepayment(
            amount = loan.amount//loan.term,
            balance = loan.amount//loan.term,
            paid = 0,
            status = ScheduledRepaymentStatus.PENDING,
            due_date = repayment_date
        )
    assert loan.scheduled_repayments[-1] == ScheduledRepayment(
        amount=loan.amount // loan.term + (loan.amount % loan.term),
        balance=loan.amount // loan.term + (loan.amount % loan.term),
        paid=0,
        status=ScheduledRepaymentStatus.PENDING,
        due_date=repayment_date + datetime.timedelta(days=7)
    )

    assert len(loan.customer_repayments) == 0


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_create_loan_auth_fail(auth_token_and_controllers, loan_details):
    token, loan_controller, user_controller = auth_token_and_controllers
    with pytest.raises(AuthFailedException):
        loan_controller._create(headers={'x-auth-token': 'random_token'}, loan_details=loan_details)
    with pytest.raises(AuthHeaderMissingException):
        loan_controller._create(headers={}, loan_details=loan_details)

@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_fetch_by_id(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    loan = loan_controller._fetch_by_id(headers={'x-auth-token': token}, id=loan.id)
    assert loan.amount == loan_details['amount']
    assert loan.currency == loan_details['currency']
    assert loan.term == loan_details['term']

    with pytest.raises(EntityDoesNotExistException):
        loan_controller._fetch_by_id(headers={'x-auth-token': token}, id='random-id')


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_fetch_by_id_authentication_fail(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    with pytest.raises(AuthFailedException):
        loan_controller._fetch_by_id(headers={'x-auth-token': 'random_token'}, id=loan.id)


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_fetch_by_id_authorization_fail(auth_token_and_controllers, loan_details):
    token, loan_controller, user_controller = auth_token_and_controllers
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)
    user2 = user_controller._signup({'name': 'user2', 'email': 'email2', 'password': 'pw'})
    token2 = user_controller._login({'email': user2.email, 'password': 'pw'}).token

    with pytest.raises(AuthorizationError):
        loan_controller._fetch_by_id(headers={'x-auth-token': token2}, id=loan.id)


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_fetch_all(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan1 = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)
    loan2 = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    loans = loan_controller._fetch_all(headers={'x-auth-token': token})
    assert loans.count == 2
    assert loans.message == "Success"
    assert loans.loans[0] == loan2
    assert loans.loans[1] == loan1


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_fetch_all_auth_fail(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)
    loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    with pytest.raises(AuthFailedException):
        loan_controller._fetch_all(headers={'x-auth-token': 'random_token'})


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_approve_loan(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    loan_controller._approve_loan(headers={'x-admin-auth-token': 'admin-token'}, loan_id=loan.id)
    loan = loan_controller._fetch_by_id(headers={'x-auth-token': token}, id=loan.id)
    assert loan.status == LoanStatus.APPROVED


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5), dummy_loan(10000, 'INR', 3)])
def test_approve_loan_auth_fail(auth_token_and_loan_controller, loan_details):
    token, loan_controller = auth_token_and_loan_controller
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)

    with pytest.raises(AuthorizationError):
        loan_controller._approve_loan(headers={'x-admin-auth-token': token}, loan_id=loan.id)
    with pytest.raises(AuthHeaderMissingException):
        loan_controller._approve_loan(headers={}, loan_id=loan.id)


@pytest.mark.parametrize("loan_details", [dummy_loan(100, 'INR', 5)])
def test_make_customer_repayment(auth_token_and_controllers, loan_details):
    token, loan_controller, user_controller = auth_token_and_controllers
    loan = loan_controller._create(headers={'x-auth-token': token}, loan_details=loan_details)
    loan_controller._approve_loan(headers={'x-admin-auth-token': 'admin-token'}, loan_id=loan.id)
    loan = loan_controller._fetch_by_id(headers={'x-auth-token': token}, id=loan.id)


    user2 = user_controller._signup({'name': 'user2', 'email': 'email2', 'password': 'pw'})
    token2 = user_controller._login({'email': user2.email, 'password': 'pw'}).token

    with pytest.raises(AuthorizationError):
        loan_controller._make_customer_repayment(headers={'x-auth-token': token2}, loan_id=loan.id,
                                                            repayment_details={'amount': 10, 'currency': 'INR'})

    response = loan_controller._make_customer_repayment(headers={'x-auth-token': token}, loan_id=loan.id, repayment_details={'amount': 10, 'currency': 'INR'})
    assert response.scheduled_repayments[0].paid == 10
    assert response.scheduled_repayments[0].balance == 10
    assert response.scheduled_repayments[0].status == ScheduledRepaymentStatus.PENDING
    assert loan.status == LoanStatus.APPROVED
    for repayment in response.scheduled_repayments[1:]:
        assert repayment.paid == 0
        assert repayment.balance == 20
        assert repayment.status == ScheduledRepaymentStatus.PENDING

    loan_controller._make_customer_repayment(headers={'x-auth-token': token}, loan_id=loan.id, repayment_details={'amount': 10, 'currency': 'INR'})
    assert response.scheduled_repayments[0].paid == 20
    assert response.scheduled_repayments[0].balance == 0
    assert response.scheduled_repayments[0].status == ScheduledRepaymentStatus.PAID
    assert loan.status == LoanStatus.APPROVED
    for repayment in response.scheduled_repayments[1:]:
        assert repayment.paid == 0
        assert repayment.balance == 20
        assert repayment.status == ScheduledRepaymentStatus.PENDING

    loan_controller._make_customer_repayment(headers={'x-auth-token': token}, loan_id=loan.id, repayment_details={'amount': 20, 'currency': 'INR'})
    assert response.scheduled_repayments[1].paid == 20
    assert response.scheduled_repayments[1].balance == 0
    assert response.scheduled_repayments[1].status == ScheduledRepaymentStatus.PAID
    assert loan.status == LoanStatus.APPROVED
    for repayment in response.scheduled_repayments[2:]:
        assert repayment.paid == 0
        assert repayment.balance == 20
        assert repayment.status == ScheduledRepaymentStatus.PENDING

    loan_controller._make_customer_repayment(headers={'x-auth-token': token}, loan_id=loan.id, repayment_details={'amount': 25, 'currency': 'INR'})
    assert response.scheduled_repayments[2].paid == 20
    assert response.scheduled_repayments[2].balance == 0
    assert response.scheduled_repayments[2].status == ScheduledRepaymentStatus.PAID
    assert response.scheduled_repayments[3].paid == 5
    assert response.scheduled_repayments[3].balance == 15
    assert response.scheduled_repayments[3].status == ScheduledRepaymentStatus.PENDING
    assert loan.status == LoanStatus.APPROVED
    for repayment in response.scheduled_repayments[4:]:
        assert repayment.paid == 0
        assert repayment.balance == 20
        assert repayment.status == ScheduledRepaymentStatus.PENDING

    loan_controller._make_customer_repayment(headers={'x-auth-token': token}, loan_id=loan.id, repayment_details={'amount': 35, 'currency': 'INR'})
    assert response.scheduled_repayments[3].paid == 20
    assert response.scheduled_repayments[3].balance == 0
    assert response.scheduled_repayments[3].status == ScheduledRepaymentStatus.PAID
    assert response.scheduled_repayments[4].paid == 20
    assert response.scheduled_repayments[4].balance == 0
    assert response.scheduled_repayments[4].status == ScheduledRepaymentStatus.PAID

    loan = loan_controller._fetch_by_id(headers={'x-auth-token': token}, id=loan.id)
    assert loan.status == LoanStatus.PAID
