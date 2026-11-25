from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import DatabaseSession
from app.modules.users import service
from app.modules.users.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users",tags=["Users"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: DatabaseSession,
):
    try:
        user = service.register_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )

        return user

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc