from typing import Any, Annotated
from fastapi import APIRouter, Depends, status
from telemetry import telemetry, Telemetry
from sqlalchemy.ext.asyncio import AsyncSession
from db import database, crud, schemas
import httpx

router = APIRouter()

card_storage = {}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Card)
async def create_card(card: schemas.CardCreate, db: AsyncSession = Depends(database.get_db)):
    card_model = await crud.create_card(db=db, card=card)
    return card_model

@router.get("/{card_name}", response_model=schemas.CardImage)
async def get_card_by_name(card_name: str, telemetry: Annotated[Telemetry, Depends(telemetry)], db: AsyncSession = Depends(database.get_db)):
    card_model = await crud.get_card_by_name(db=db, card_name=card_name)
    card = card_model[0]
    if card_model is None:
        return status.HTTP_404_NOT_FOUND
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.scryfall.com/cards/named?fuzzy={card_name}")
        telemetry.request_counter.add(1, { "status_code": r.status_code, "card_name": card_name, "client":"Scryfall"})
        img_uri = None
        if r.status_code == 200:
            response = r.json()
            img_uri = response.get("image_uris", {}).get("normal")
    card = schemas.CardImage(
        id=card.id,
        flavor_text=card.flavor_text, 
        name=card.name,
        mana_cost=card.mana_cost,
        oracle_text=card.oracle_text,
        rarity=card.rarity, 
        card_types=card.card_types,
        img=img_uri
    )
    return card