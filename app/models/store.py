from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.store_user import StoreUserLink


class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_hash: str
    access_token: str
    scope: str
    users: List["User"] = Relationship(back_populates="stores", link_model=StoreUserLink)