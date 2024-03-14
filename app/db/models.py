from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, Mapped
from .database import Base
from typing import List

card_type_tbl = Table(
    "card_type_tbl",
    Base.metadata,
    Column("card_id", ForeignKey("cards.id")),
    Column("card_types_id", ForeignKey("card_types.id"))
)

class CardType(Base):
    __tablename__ = "card_types"
    id = Column(Integer, primary_key=True)
    card_type: Mapped[str] = Column(String)

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    flavor_text = Column(String)
    name = Column(String)
    mana_cost = Column(Integer)
    oracle_text = Column(String)
    rarity = Column(String)
    card_types: Mapped[List[CardType]] = relationship(secondary=card_type_tbl, lazy="selectin")




