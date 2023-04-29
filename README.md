# mini-aspire
Prerequirements
===============
1. You need a linux environment with python3 installed (>= 3.9).

How to run?
==========
1. #### make run - This should be enough
    1. It installs the python venv package (might need to supply password for sudo).
    1. Creates a virtual environment by name my_env in the PWD.
    1. Activates the virtual environment
    1. Install the required python packages using pip in the virtual environment
    1. Runs the server

1. ####make clean
    1. Use this to delete the virtual environment created after you shut down the server.

How does it work?
=================
1. There are primarily two sets of APIs
    1. User APIs
    1. Loan APIs
    
1. User APIs
    1. Sign up API
        1. API to sign up/create a user in the system.
        1. Once done, a user is stored in the database.
    1. Login API
        1. API to login a user into the system.
        1. Once done, a token is generated and sent in the response
        1. The generated token is expected to be sent as __x-auth-token__ header for authentication/authorization purposes in subsequent API calls.
    1. Fetch user API
        1. API to fetch the details of a single user based on their __id__.
        1. This API requires __x-auth-token__ to authenticate/authorize(verify that a user is fetching their own details).
    1. Fetch all users API
        1. API to fetch the details of all the users in the system.
        1. This can only be performed by the admin; and requires a __x-admin-auth-token__ header.
 
 1. Loan APIs
    1. Request loan API
        1. API to allow a user to request a loan; creates a loan in the system.
        1. Requires __x-auth-token__ to authenticate the user.
    1. Fetch loan API
        1. API to fetch a loan of a user based on loan id.
        1. Requires __x-auth-token__ to authenticate/authorize the access for the user.
    1. Fetch all loans API
        1. API to fetch all the loans of particular user.
        1. Requires __x-auth-token__ header to authenticate/authorize and determine the requesting user, based on which the loans will be returned.
    1. Approve loan API
        1. API to approve a loan.
        1. Requires __x-admin-auth-token__ header to authenticate/authorize only an admin can perfom this action.
    1. Make customer repayment API
        1. API to allow a user to repay back for one of their loans.
        1. Requires __x-auth-token__ header for authentication/authorization.
        
Design choices
==============
1. Chose to create decorators for authentication/authorization as it is closest to a middleware in flask. Also it easily allows us to add auth to a new API.
2. Repayment strategy is being injected into the loan service so that if we want to change it, we need only implement the strategy and plug it in.
3. The db layer also has been abstracted out and injected into the services. By default, I'm using in memory db for simplicity, but if we need a MySQL storage, we need only implement and plug it in.
              