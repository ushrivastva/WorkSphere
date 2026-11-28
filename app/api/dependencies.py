from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import HTTPAuthorizationCredentials
from app.database.session import get_db
from app.core.security import oauth2_scheme, verify_access_token
from app.modules.users import repository
from app.modules.users.models import User

DatabaseSession = Annotated[Session, Depends(get_db)]

def get_current_user(
    token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(oauth2_scheme)
    ],
    db: DatabaseSession
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception

    try: 
        payload = verify_access_token(token.credentials)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception

        user = repository.get_user_by_id(db, int(user_id))

        
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise credentials_exception

        return user

    except (ValueError, TypeError):
        raise credentials_exception


