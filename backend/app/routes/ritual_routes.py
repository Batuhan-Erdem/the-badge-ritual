import time

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


def log_step(message: str):
    print(f"[RITUAL DEBUG] {message}", flush=True)


@router.post("/create")
def create_ritual(request: RitualRequest):
    started_at = time.time()

    try:
        log_step("Request received.")
        log_step("Step 1 started: LLM ritual response generation.")

        ritual_result = generate_ritual_response(
            badge=request.badge,
            origin=request.origin,
            cost=request.cost,
        )

        log_step("Step 1 completed: LLM ritual response generated.")
        log_step(f"Door material: {ritual_result.get('doorMaterial', 'missing')}")
        log_step("Step 2 started: Image generation.")

        generated_file_name = generate_ritual_image(
            ritual_result["imagePrompt"]
        )

        log_step("Step 2 completed: Image generated.")

        image_url = f"http://127.0.0.1:8000/generated/{generated_file_name}"

        log_step("Step 3 started: TTS voice + ambience generation.")

        generated_audio_file_name = generate_ritual_voice(
            tts_text=ritual_result["ttsText"],
            door_material=ritual_result.get("doorMaterial", "old_wood"),
        )

        log_step("Step 3 completed: Audio generated.")

        audio_url = (
            f"http://127.0.0.1:8000/generated/audio/{generated_audio_file_name}"
        )

        elapsed = round(time.time() - started_at, 2)
        log_step(f"Ritual completed in {elapsed} seconds.")

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
        log_step(f"Ritual generation failed: {error}")

        raise HTTPException(
            status_code=500,
            detail=f"The ritual could not be generated: {error}",
        )