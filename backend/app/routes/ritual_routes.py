from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/ritual", tags=["ritual"])


class RitualRequest(BaseModel):
    badge: str
    origin: str
    cost: str


@router.post("/create")
def create_ritual(request: RitualRequest):
    return {
        "badgeTitle": "The Badge of Silent Strength",
        "historicalEcho": (
            "In 1973, another badge became too heavy to wear. "
            "Not because it had no meaning, but because meaning itself had become heavy. "
            "Your badge carries a similar silence: it once gave you a role, "
            "but now it asks to be set down."
        ),
        "releaseText": (
            "You have carried this badge long enough. "
            "It may have protected you once, but not every protection is meant to become a prison. "
            "At the edge of this door, you do not erase who you were. "
            "You simply put down what no longer lets you breathe."
        ),
        "imagePrompt": (
            "A worn wooden door standing alone in a dusty twilight landscape, "
            "an old metal badge lying at the threshold, cinematic 1970s western mood, "
            "melancholic folk atmosphere, symbolic, painterly, warm amber and dark brown tones."
        ),
        "ttsText": (
            "You have carried this badge long enough. "
            "At the edge of this door, you do not erase who you were. "
            "You simply put down what no longer lets you breathe."
        ),
        "imageUrl": None,
        "audioUrl": None,
        "userInput": {
            "badge": request.badge,
            "origin": request.origin,
            "cost": request.cost,
        },
    }
