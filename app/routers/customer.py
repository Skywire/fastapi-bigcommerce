from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.dependencies import verified_customer_bearer

router = APIRouter(
    prefix="/customer",
    tags=['Customer']
)


@router.get('/me')
def me(user_data: dict = Depends(verified_customer_bearer)):
    return user_data
