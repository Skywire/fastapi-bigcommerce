from typing import Optional

from sqlmodel import SQLModel, Field


class StoreUserScope(SQLModel, table=True):
    __tablename__ = 'store_user_scope'
    store_id: Optional[int] = Field(
        default=None, foreign_key="store.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    is_owner: bool = Field(default=False)