from typing import Optional

from sqlmodel import SQLModel, Field


class StoreUserLink(SQLModel, table=True):
    __tablename__ = 'store_user'
    store_id: Optional[int] = Field(
        default=None, foreign_key="store.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    admin: bool = Field(default=False)
