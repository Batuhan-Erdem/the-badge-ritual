from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import generate_ritual_response

router = APIRouter(prefix="/api/ritual", tags=["ritual"])


class RitualRequest(BaseModel):
    badge: str
    origin: str
    cost: str


@router.post("/create")
def create_ritual(request: RitualRequest):
    try:
        ritual_result = generate_ritual_response(
            badge=request.badge,
            origin=request.origin,
            cost=request.cost,
        )

        return {
            **ritual_result,
            "imageUrl": None,
            "audioUrl": None,
            "userInput": {
                "badge": request.badge,
                "origin": request.origin,
                "cost": request.cost,
            },
        }

    except Exception as error:
        print("Ritual generation error:", error)

        raise HTTPException(
            status_code=500,
            detail="The ritual could not be generated.",
        )
