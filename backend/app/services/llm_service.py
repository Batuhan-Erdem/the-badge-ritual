import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.prompts.ritual_prompt import build_ritual_prompt
from app.prompts.image_prompt import strengthen_image_prompt
from app.services.rag_service import build_full_context


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def generate_ritual_response(badge: str, origin: str, cost: str) -> dict:
    """
    Generates the ritual response using RAG context + OpenAI LLM.
    Returns a dictionary with:
    badgeTitle, historicalEcho, releaseText, imagePrompt, ttsText.
    """

    full_context = build_full_context(
        badge=badge,
        origin=origin,
        cost=cost,
    )

    ritual_prompt = build_ritual_prompt(full_context)

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": "You are a careful JSON-generating ritual writer for an interactive digital artwork.",
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
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "badgeTitle": {
                            "type": "string"
                        },
                        "historicalEcho": {
                            "type": "string"
                        },
                        "releaseText": {
                            "type": "string"
                        },
                        "imagePrompt": {
                            "type": "string"
                        },
                        "ttsText": {
                            "type": "string"
                        },
                    },
                    "required": [
                        "badgeTitle",
                        "historicalEcho",
                        "releaseText",
                        "imagePrompt",
                        "ttsText",
                    ],
                },
                "strict": True,
            }
        },
    )

    raw_text = response.output_text
    ritual_data = json.loads(raw_text)

    ritual_data["imagePrompt"] = strengthen_image_prompt(
        ritual_data["imagePrompt"]
    )

    return ritual_data

