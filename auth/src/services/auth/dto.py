from dataclasses import dataclass


@dataclass
class UserCreateDTO:
    username: str
    email: str
    password: str


@dataclass
class UserResponseDTO:
    id: int
    username: str
    email: str
