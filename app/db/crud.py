from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

async def get_card_by_name(db: Session, card_name: str):
    stmt_return = await db.execute(select(models.Card).where(models.Card.name == card_name))
    return stmt_return.first()

async def create_card(db: Session, card: schemas.CardCreate) -> models.Card:
    card_type_names = [card_type.value for card_type in card.card_types]
    card_types = (await db.execute(select(models.CardType).where(models.CardType.card_type.in_(card_type_names)))).scalars().all()
    card_model = models.Card(
        flavor_text=card.flavor_text, 
        name=card.name, 
        card_types=card_types, 
        mana_cost=card.mana_cost, 
        oracle_text=card.oracle_text, 
        rarity=card.rarity
    )
    db.add(card_model)
    await db.commit()
    await db.refresh(card_model)
    return card_model