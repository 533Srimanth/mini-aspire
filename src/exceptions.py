from typing import Any


class EntityDoesNotExistException(Exception):
    def __init__(self, entity: str, identifiers: Any = None):
        if identifiers is None:
            message = f"No such {entity} found"
        else:
            message = f"No {entity} found for {identifiers.__dict__}"
        super().__init__(message)


class AuthHeaderMissingException(Exception):
    def __init__(self, header):
        super().__init__(f"Authentication failed - header '{header}' is missing")


class AuthFailedException(Exception):
    def __init__(self):
        super().__init__(f"Authentication failed")

