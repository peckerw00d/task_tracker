from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.services.auth.token_service import TokenService
from src.api.schemas.auth_schemas import TokenResponseSchema, UserLoginSchema
from src.services.auth.dto import UserCreateDTO, UserCredentialsDTO
from src.api.schemas import UserRegistrationSchema

from src.services.auth.auth_service import AuthService
from src.services.auth.exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
    UsernameAlreadyInUse,
)


bearer_scheme = HTTPBearer()

router = APIRouter(route_class=DishkaRoute)


@router.post("/registration")
async def registration(
    data: UserRegistrationSchema, auth_service: FromDishka[AuthService]
):
    try:
        user_data = UserCreateDTO(**data.model_dump())
        new_user = await auth_service.registration(data=user_data)

        return {"message": "You have successfully registered!"}

    except UserAlreadyExists as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists!"
        )

    except UsernameAlreadyInUse as err:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already in use!"
        )


@router.post("/login")
async def login(
    data: UserLoginSchema, auth_service: FromDishka[AuthService], response: Response
) -> TokenResponseSchema:
    try:
        credentials = UserCredentialsDTO(**data.model_dump())
        access_token = await auth_service.login(credentials=credentials)

        return {"access_token": access_token}

    except InvalidCredentials as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!"
        )


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "You have successfully logged out!"}


@router.get("/validate")
async def validate_token(
    token_service: FromDishka[TokenService],
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        return await token_service.validate_token(token=token.credentials)

    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err))
