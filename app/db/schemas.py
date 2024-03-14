from pydantic import BaseModel, ConfigDict
from typing import Union
from enum import Enum

class CardTypeEnum(Enum):
    Artifact = "Artifact"
    Enchantment = "Enchantment"
    Creature = "Creature"
    Instant = "Instant"
    Sorcery = "Sorcery"
    Land = "Land"


class CardType(BaseModel):
    id: int
    card_type: CardTypeEnum
    model_config = ConfigDict(from_attributes=True)


class CardBase(BaseModel):
    flavor_text: str
    name: str
    mana_cost: int
    oracle_text: str
    rarity: str

class CardCreate(CardBase):
    card_types: list[CardType] = []

class Card(CardBase):
    id: int
    card_types: list[CardType] = []

    model_config = ConfigDict(from_attributes=True)

class CardImage(Card):
    img: Union[str, None]