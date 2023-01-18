import jwt
from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from sqlalchemy.orm import Session

from api.schemas.auth import (
    UserTokenResponse,
    UserResponse,
    UserCreateRequest,
    TokenPayload
)
from api.settings import (
    JWT_SECRET_KEY,
    ALGORITHM
)
from database.db import get_db
from database.models import User
from database.hasher import (
    verify_password,
    create_access_token,
    create_refresh_token
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login", 
    scheme_name="JWT"
)


router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse)
def register(data: UserCreateRequest, db: Session=Depends(get_db)):
    user = db.query(User).filter(
        User.username==data.username
    ).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    user = data.insert(db)
    return UserResponse.from_db_instance(user)


@router.post("/login", response_model=UserTokenResponse)
def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(User).filter(
        User.username==user_data.username
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    hashed_pass = user.password
    if not verify_password(user_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email)
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)
) -> UserResponse:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.query(User).filter(User.email==token_data.sub).first()
    return UserResponse.from_db_instance(user)
 