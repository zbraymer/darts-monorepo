from fastapi import APIRouter
from .. import schemas
from ..utils.scoring import calculate_score

router = APIRouter()


@router.get("/status")
def game_status():
    return {"message": "Game status endpoint"}


@router.get("/throw")
def process_throw(radius: float, angle: float):
    return calculate_score(radius, angle)
