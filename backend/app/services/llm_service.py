import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts.ritual_prompt import build_ritual_prompt
from app.prompts.image_prompt import strengthen_image_prompt
from app.services.rag_service import build_full_context


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    USE_OPENAI = True
else:
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
    MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.1")
    USE_OPENAI = False


def generate_ritual_response(badge: str, origin: str, cost: str) -> dict:
    """
    Generates the ritual response using RAG context + LLM.

    Returns a dictionary with:
    - badgeTitle
    - historicalEcho
    - releaseText
    - imagePrompt
    - ttsText
    - doorGuidance
    - badgePlacementGuidance
    - afterBadgeGuidance
    - knockGuidance
    - doorResponseGuidance
    - doorMaterial
    """

    full_context = build_full_context(
        badge=badge,
        origin=origin,
        cost=cost,
    )

    ritual_prompt = build_ritual_prompt(full_context)

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "badgeTitle": {"type": "string"},
            "historicalEcho": {"type": "string"},
            "releaseText": {"type": "string"},
            "imagePrompt": {"type": "string"},
            "ttsText": {"type": "string"},
            "doorGuidance": {"type": "string"},
            "badgePlacementGuidance": {"type": "string"},
            "afterBadgeGuidance": {"type": "string"},
            "knockGuidance": {"type": "string"},
            "doorResponseGuidance": {"type": "string"},
            "doorMaterial": {
                "type": "string",
                "enum": [
                    "old_wood",
                    "heavy_wood",
                    "rusted_metal",
                    "dark_iron",
                    "fragile_wood"
                ]
            },
        },
        "required": [
            "badgeTitle",
            "historicalEcho",
            "releaseText",
            "imagePrompt",
            "ttsText",
            "doorGuidance",
            "badgePlacementGuidance",
            "afterBadgeGuidance",
            "knockGuidance",
            "doorResponseGuidance",
            "doorMaterial",
        ],
    }

    if USE_OPENAI:
        response = client.responses.create(
            model=MODEL_NAME,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful JSON-generating ritual writer for an "
                        "interactive digital artwork. Always return valid JSON "
                        "that matches the requested schema."
                    ),
                },
                {
                    "role": "user",
                    "content": ritual_prompt,
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "ritual_response",
                    "schema": schema,
                    "strict": True,
                }
            },
        )
        raw_text = response.output_text
    else:
        schema_prompt = "\n\nEnsure your response strictly matches this JSON schema:\n" + json.dumps(schema)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful JSON-generating ritual writer for an "
                        "interactive digital artwork. Always return valid JSON "
                        "that matches the requested schema."
                    ) + schema_prompt,
                },
                {
                    "role": "user",
                    "content": ritual_prompt,
                },
            ],
            response_format={"type": "json_object"},
        )
        raw_text = response.choices[0].message.content

    ritual_data = json.loads(raw_text)

    ritual_data["imagePrompt"] = strengthen_image_prompt(
        ritual_data["imagePrompt"]
    )

    return ritual_data
