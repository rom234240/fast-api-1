from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AdvertisementBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

class Advertisement(AdvertisementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime