import time
import concurrent.futures

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import generate_ritual_response
from app.services.image_service import generate_ritual_image, generate_open_door_image
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

        image_prompt = ritual_result["imagePrompt"]

        # Önce kapalı kapıyı üret (img2img için base64'e ihtiyacımız var)
        log_step("Step 2 started: Closed door image generation.")
        generated_file_name, closed_door_b64 = generate_ritual_image(image_prompt)
        log_step("Step 2 completed: Closed door image generated.")

        # Sonra açık kapı (img2img) + ses paralel çalışsın
        log_step("Steps 3 & 4 started: Parallel open-door (img2img) and TTS generation.")

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_open_image = executor.submit(
                generate_open_door_image, image_prompt, closed_door_b64
            )
            future_audio = executor.submit(
                generate_ritual_voice,
                tts_text=ritual_result["ttsText"],
                door_material=ritual_result.get("doorMaterial", "old_wood")
            )

            generated_open_file_name = future_open_image.result()
            generated_audio_file_name = future_audio.result()

        log_step("Steps 3 & 4 completed: Parallel generation finished.")

        base_url = "http://127.0.0.1:8000"
        image_url = f"{base_url}/generated/{generated_file_name}"
        open_image_url = f"{base_url}/generated/{generated_open_file_name}"
        audio_url = f"{base_url}/generated/audio/{generated_audio_file_name}"

        elapsed = round(time.time() - started_at, 2)
        log_step(f"Ritual completed in {elapsed} seconds.")

        return {
            **ritual_result,
            "imageUrl": image_url,
            "openImageUrl": open_image_url,
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