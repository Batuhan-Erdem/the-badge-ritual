import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0,
)

TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "onyx")

AUDIO_DIR = Path(__file__).resolve().parent.parent.parent / "generated" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def _prepare_tts_text(tts_text: str) -> str:
    """
    Keeps TTS short enough to avoid long blocking audio generation.
    """
    clean_text = (tts_text or "").strip()

    if not clean_text:
        return "The door is quiet. The badge has been named. You may approach the threshold slowly."

    max_length = 900

    if len(clean_text) > max_length:
        return clean_text[:max_length].rsplit(" ", 1)[0] + "."

    return clean_text


def generate_ritual_voice(tts_text: str, door_material: str = "old_wood") -> str:
    """
    Stable production version.

    Important:
    - This function generates ONLY the spoken TTS narration.
    - It does NOT generate backend ambience.
    - It does NOT mix audio files.
    - Background music/ambience is handled by the frontend Web Audio system.

    Why:
    Backend voice + ambience mixing was causing long blocking requests.
    This keeps ritual generation fast and stable.
    """

    print("[TTS DEBUG] generate_ritual_voice entered.", flush=True)
    print(f"[TTS DEBUG] Door material received: {door_material}", flush=True)
    print("[TTS DEBUG] Voice-only TTS generation started.", flush=True)

    unique_id = uuid.uuid4().hex
    voice_file_name = f"ritual_voice_{unique_id}.mp3"
    voice_path = AUDIO_DIR / voice_file_name

    prepared_text = _prepare_tts_text(tts_text)

    try:
        with client.audio.speech.with_streaming_response.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=prepared_text,
            response_format="mp3",
            instructions=(
                "Speak like a calm ritual narrator talking directly to a close friend. "
                "Use a natural, warm, intimate, human voice. "
                "Do not sound robotic, theatrical, or like a news reader. "
                "Use gentle pauses. "
                "The tone should be serious, soft, cinematic, and emotionally grounded. "
                "Do not sound overly motivational. "
                "The listener should feel accompanied, not instructed."
            ),
        ) as response:
            response.stream_to_file(voice_path)

        print("[TTS DEBUG] Voice-only TTS generation completed.", flush=True)
        print(f"[TTS DEBUG] Voice file created: {voice_file_name}", flush=True)

        return voice_file_name

    except Exception as error:
        print(f"[TTS DEBUG] Voice generation failed: {error}", flush=True)
        raise error