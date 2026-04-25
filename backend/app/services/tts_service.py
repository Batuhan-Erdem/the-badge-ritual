import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "onyx")

AUDIO_DIR = Path(__file__).resolve().parent.parent.parent / "generated" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_ritual_voice(tts_text: str) -> str:
    """
    Generates voice narration from ritual text,
    saves it under backend/generated/audio,
    and returns the saved filename.
    """
    file_name = f"ritual_voice_{uuid.uuid4().hex}.mp3"
    file_path = AUDIO_DIR / file_name

    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=tts_text,
        instructions=(
            "Speak slowly and calmly, like a quiet ritual narrator. "
            "The tone should be intimate, cinematic, serious, and gentle. "
            "Do not sound cheerful or motivational."
        ),
    ) as response:
        response.stream_to_file(file_path)

    return file_name

