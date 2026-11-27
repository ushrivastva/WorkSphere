from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from app.modules.users import repository
from sqlalchemy.exc import IntegrityError

password_hash = PasswordHash.recommended()

def register_user(
        db: Session,
        username: str,
        email: str,
        password: str,
):
    existing_email = repository.get_user_by_email(db, email)

    if existing_email:
        raise ValueError("Email alredy registerd")

    existing_username = repository.get_user_by_username(db,  username)

    if existing_username:
        raise ValueError("Username already taken")

    hashed_password = password_hash.hash(password)

    try:
        return repository.create_user(
            db=db,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

    except IntegrityError as exc:
        db.rollback()

        raise ValueError(
            "Email or username already exists"
        ) from exc

def login_user(db:Session, email: str, password: str):
    # ----> we use this for,"Find user by email"

    user = repository.get_user_by_email(db, email)

    if not user:
        raise ValueError("Invalid email or password")

    if not password_hash.verify(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    return user

