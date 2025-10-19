from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from app.database.database import get_db
from app.models.advertisement import Advertisement
from app.schemas.advertisement import Advertisement as AdvertisementSchema, AdvertisementCreate, AdvertisementUpdate

router = APIRouter(prefix="/advertisement", tags=["advertisements"])

@router.post("", response_model=AdvertisementSchema)
async def create_advertisement(
    advertisement: AdvertisementCreate,
    db: AsyncSession = Depends(get_db)
):
    db_advertisement = Advertisement(**advertisement.model_dump())
    db.add(db_advertisement)
    await db.commit()
    await db.refresh(db_advertisement)
    return db_advertisement

@router.get("/{advertisement_id}", response_model=AdvertisementSchema)
async def get_advertisement(
    advertisement_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Advertisement).where(Advertisement.id == advertisement_id))
    advertisement = result.scalar_one_or_none()
    
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    return advertisement

@router.patch("/{advertisement_id}", response_model=AdvertisementSchema)
async def update_advertisement(
    advertisement_id: int,
    advertisement_update: AdvertisementUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Advertisement).where(Advertisement.id == advertisement_id))
    advertisement = result.scalar_one_or_none()
    
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    update_data = advertisement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(advertisement, field, value)
    
    await db.commit()
    await db.refresh(advertisement)
    return advertisement

@router.delete("/{advertisement_id}")
async def delete_advertisement(
    advertisement_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Advertisement).where(Advertisement.id == advertisement_id))
    advertisement = result.scalar_one_or_none()
    
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    
    await db.delete(advertisement)
    await db.commit()
    
    return {"message": "Advertisement deleted successfully"}

@router.get("", response_model=list[AdvertisementSchema])
async def search_advertisements(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Advertisement)
    
    conditions = []
    if title:
        conditions.append(Advertisement.title.ilike(f"%{title}%"))
    if description:
        conditions.append(Advertisement.description.ilike(f"%{description}%"))
    if author:
        conditions.append(Advertisement.author.ilike(f"%{author}%"))
    if min_price is not None:
        conditions.append(Advertisement.price >= min_price)
    if max_price is not None:
        conditions.append(Advertisement.price <= max_price)
    
    if conditions:
        query = query.where(or_(*conditions))
    
    result = await db.execute(query)
    advertisements = result.scalars().all()
    return advertisements