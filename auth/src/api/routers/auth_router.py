from fastapi import APIRouter, status, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.services.auth.dto import UserCreateDTO
from src.api.schemas import UserRegistrationSchema

from src.services.auth.auth_service import AuthService
from src.services.auth.exceptions import UserAlreadyExists

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
