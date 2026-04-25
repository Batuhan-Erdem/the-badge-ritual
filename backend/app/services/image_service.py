import base64
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")

GENERATED_DIR = Path(__file__).resolve().parent.parent.parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)


def generate_ritual_image(image_prompt: str) -> str:
    """
    Generates an image using OpenAI Image API,
    saves it under backend/generated,
    and returns the saved filename.
    """
    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=image_prompt,
        size="1024x1024"
    )

    image_b64 = response.data[0].b64_json

    file_name = f"ritual_{uuid.uuid4().hex}.png"
    file_path = GENERATED_DIR / file_name

    with open(file_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_b64))

    return file_name
