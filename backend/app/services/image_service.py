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


def generate_ritual_image(image_prompt: str) -> tuple[str, str]:
    """
    Generates a closed door image.
    Returns (filename, base64_string) so the b64 can be reused for img2img.
    """
    if USE_OPENAI:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=image_prompt,
            size="1024x1024"
        )
        image_b64 = response.data[0].b64_json
    else:
        image_b64 = _generate_sd_image(image_prompt)

    file_name = f"ritual_{uuid.uuid4().hex}.png"
    file_path = GENERATED_DIR / file_name

    with open(file_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_b64))

    return file_name, image_b64


def generate_open_door_image(base_image_prompt: str, closed_door_b64: str = None) -> str:
    """
    Generates an 'open door' version using img2img.
    Takes the closed door image as input and modifies it to show it ajar.
    """
    open_door_prompt = (
        "The same door, now slightly open, ajar by 20 degrees. "
        "Warm golden ethereal light spills through the gap from behind. "
        "The badge is still on the ground at the threshold. "
        "Same cinematic style, same materials, same lighting, same composition. "
        "Quiet, emotional, symbolic. Painterly but realistic."
    )

    negative_prompt = (
        "different door, different material, different room, "
        "people, text, logos, watermark"
    )

    if USE_OPENAI:
        # OpenAI doesn't support img2img well, fall back to full prompt generation
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=f"{base_image_prompt}\n\nThe door is now slightly open, ajar. Warm golden light spills through the gap.",
            size="1024x1024"
        )
        image_b64 = response.data[0].b64_json
    else:
        if not closed_door_b64:
            # Fallback: txt2img ile üret
            image_b64 = _generate_sd_image(base_image_prompt + "\n\nThe door is ajar, slightly open, warm light through gap.")
        else:
            # img2img: kapalı kapıyı girdi olarak kullan
            img2img_url = SD_API_URL.replace("txt2img", "img2img")
            payload = {
                "init_images": [closed_door_b64],
                "prompt": open_door_prompt,
                "negative_prompt": negative_prompt,
                "denoising_strength": 0.45,  # Düşük = orijinal kapıya daha yakın
                "steps": 20,
                "width": 512,
                "height": 512,
                "cfg_scale": 7,
            }
            with httpx.Client() as client_http:
                print("[IMAGE DEBUG] Sending img2img request for open door...", flush=True)
                res = client_http.post(img2img_url, json=payload, timeout=None)
                res.raise_for_status()
                image_b64 = res.json()["images"][0]
                print("[IMAGE DEBUG] img2img open door received.", flush=True)

                # Upscale
                upscale_url = SD_API_URL.replace("txt2img", "extra-single-image")
                try:
                    upscale_res = client_http.post(
                        upscale_url,
                        json={"upscaling_resize": 2, "upscaler_1": "Lanczos", "image": image_b64},
                        timeout=None
                    )
                    upscale_res.raise_for_status()
                    image_b64 = upscale_res.json().get("image", image_b64)
                    print("[IMAGE DEBUG] Open door upscale complete.", flush=True)
                except Exception as e:
                    print(f"[IMAGE DEBUG] Open door upscale failed: {e}", flush=True)

    file_name = f"ritual_open_{uuid.uuid4().hex}.png"
    file_path = GENERATED_DIR / file_name

    with open(file_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_b64))

    print(f"[IMAGE DEBUG] Open door image created: {file_name}", flush=True)
    return file_name



def _generate_sd_image(prompt: str) -> str:
    """Shared SD generation logic with upscaling."""
    payload = {
        "prompt": prompt,
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

    return image_b64
