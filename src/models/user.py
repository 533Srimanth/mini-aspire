from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str

    def to_user_response(self):
        return UserResponse(
            id = self.id,
            name = self.name,
            email = self.email
        )


@dataclass_json
@dataclass
class UserSignUpRequest:
    name: str
    email: str
    password: str


@dataclass_json
@dataclass
class UserLoginRequest:
    email: str
    password: str


@dataclass
class UserResponse:
    id: str
    name: str
    email: str


@dataclass
class UsersResponse:
    message: str
    count: int
    users: list[UserResponse]


@dataclass
class UserLoginResponse:
    message: str
    token: str
    user: UserResponse

