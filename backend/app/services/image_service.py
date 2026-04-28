import base64
import os
import uuid
import httpx
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
    USE_OPENAI = True
else:
    SD_API_URL = os.getenv("SD_API_URL", "http://127.0.0.1:7860/sdapi/v1/txt2img")
    USE_OPENAI = False

GENERATED_DIR = Path(__file__).resolve().parent.parent.parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)


def generate_ritual_image(image_prompt: str) -> str:
    """
    Generates an image using OpenAI Image API or Stable Diffusion,
    saves it under backend/generated,
    and returns the saved filename.
    """
    if USE_OPENAI:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024"
        )
        image_b64 = response.data[0].b64_json
    else:
        # Fallback to Stable Diffusion API
        payload = {
            "prompt": image_prompt,
            "steps": 15,
            "width": 512,
            "height": 512
        }
        with httpx.Client() as client_http:
            print("[IMAGE DEBUG] Sending request to SD API...", flush=True)
            res = client_http.post(SD_API_URL, json=payload, timeout=None)
            res.raise_for_status()
            image_b64 = res.json()["images"][0]
            print("[IMAGE DEBUG] Received response from SD API.", flush=True)
            
            upscale_url = SD_API_URL.replace("txt2img", "extra-single-image")
            upscale_payload = {
                "upscaling_resize": 2,
                "upscaler_1": "Lanczos",
                "image": image_b64
            }
            print("[IMAGE DEBUG] Sending request to SD Upscale API...", flush=True)
            try:
                upscale_res = client_http.post(upscale_url, json=upscale_payload, timeout=None)
                upscale_res.raise_for_status()
                image_b64 = upscale_res.json().get("image", image_b64)
                print("[IMAGE DEBUG] Upscale complete.", flush=True)
            except Exception as e:
                print(f"[IMAGE DEBUG] Upscale failed, using original 512x512 image: {e}", flush=True)

    file_name = f"ritual_{uuid.uuid4().hex}.png"
    file_path = GENERATED_DIR / file_name

    with open(file_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_b64))

    return file_name
