from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.dependencies import verified_admin_bearer

router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)

@router.get('/me')
def me(user_data: dict = Depends(verified_admin_bearer)):
    return user_data