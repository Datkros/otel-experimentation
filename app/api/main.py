from fastapi import APIRouter
from api.routes import cards

api_router = APIRouter()
api_router.include_router(cards.router, prefix="/card", tags=["cards"])