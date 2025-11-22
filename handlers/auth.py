from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from schema import UserLoginSchema, UserCreateSchema
from service import AuthService
from dependecy import get_auth_service
from exceptions import UserNotCorrectPasswordException, UserNotFoundException


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=UserLoginSchema
)

async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        user_login_data = auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
            )
    return auth_service.login(body.username, body.password)


