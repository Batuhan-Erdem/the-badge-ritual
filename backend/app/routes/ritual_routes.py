from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import generate_ritual_response
from app.services.image_service import generate_ritual_image
from app.services.tts_service import generate_ritual_voice

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

        generated_file_name = generate_ritual_image(
            ritual_result["imagePrompt"]
        )

        image_url = f"http://127.0.0.1:8000/generated/{generated_file_name}"

        generated_audio_file_name = generate_ritual_voice(
            ritual_result["ttsText"]
        )

        audio_url = (
            f"http://127.0.0.1:8000/generated/audio/{generated_audio_file_name}"
        )

        return {
            **ritual_result,
            "imageUrl": image_url,
            "audioUrl": audio_url,
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
