class EntityDoesNotExistException(Exception):
    def __init__(self, entity: str, identifiers: dict = None):
        if identifiers is None:
            message = f"No such {entity} found"
        else:
            message = f"No {entity} found for {identifiers}"
        super().__init__(message)


class AuthHeaderMissingException(Exception):
    def __init__(self, header: str):
        super().__init__(f"Authentication failed - header '{header}' is missing")


class AuthFailedException(Exception):
    def __init__(self):
        super().__init__("Authentication failed")


class AuthorizationError(Exception):
    def __init__(self):
        super().__init__("Unauthorized action")

