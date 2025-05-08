from pydantic import BaseModel, ConfigDict


class UserBaseSchema(BaseModel):
    username: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserRegistrationSchema(UserLoginSchema):
    email: str


class UserResponseSchema(UserBaseSchema):
    id: str

    class Config:
        model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
