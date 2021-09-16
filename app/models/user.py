from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.store_user import StoreUserLink


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bc_id: int
    email: str
    stores: List["Store"] = Relationship(back_populates="users", link_model=StoreUserLink)