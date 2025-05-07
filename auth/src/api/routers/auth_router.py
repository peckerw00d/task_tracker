from fastapi import APIRouter, Response, status, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.api.schemas.auth_schemas import UserLoginSchema
from src.services.auth.dto import UserCreateDTO, UserCredentialsDTO
from src.api.schemas import UserRegistrationSchema

from src.services.auth.auth_service import AuthService
from src.services.auth.exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
    UsernameAlreadyInUse,
)

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
):
    try:
        credentials = UserCredentialsDTO(**data.model_dump())
        access_token = await auth_service.login(credentials=credentials)

        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return {"message": "You have successfully logged in!"}

    except InvalidCredentials as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!"
        )


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "You have successfully logged out!"}
