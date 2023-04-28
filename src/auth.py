from exceptions import AuthHeaderMissingException, AuthFailedException, EntityDoesNotExistException


def token_required(func):
    def decorator(self, headers, *args, **kwargs):
        if "x-auth-token" not in headers:
            raise AuthHeaderMissingException('x-auth-token')

        try:
            token = headers["x-auth-token"]
            user = self.user_service.fetch_by_token(token)
            return func(self, user, *args, **kwargs)
        except KeyError:
            raise AuthFailedException()

    return decorator


def admin_token_required(func):
    def decorator(self, headers, *args, **kwargs):
        if "x-admin-auth-token" not in headers:
            raise AuthHeaderMissingException('x-admin-auth-token')

        token = headers["x-admin-auth-token"]
        if token != self.app_config.admin_token:
            raise AuthFailedException()

        return func(self, *args, **kwargs)
    return decorator

