from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer

from jose import JWTError, jwt  # type: ignore
 

from app.core.config import settings


oauth2_scheme = HTTPBearer(auto_error=False)
def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm="HS256",
    )

    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )
        return payload

    except JWTError:
        raise ValueError("Invalid or expire access token")