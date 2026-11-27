from fastapi import APIRouter, HTTPException, status, Depends

from app.api.dependencies import DatabaseSession,get_current_user
from app.modules.users import service
from app.core.security import create_access_token
from app.modules.users.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.modules.users.models import User

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

@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin, db: DatabaseSession):
    try:
        user = service.login_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
        )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user