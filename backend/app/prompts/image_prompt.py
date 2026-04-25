def strengthen_image_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

Visual style requirements:
- symbolic digital artwork
- worn wooden door
- old metal badge near the threshold
- dusty western atmosphere
- twilight lighting
- muted 1970s cinematic mood
- melancholic folk feeling
- warm amber, dark brown, faded beige tones
- painterly but realistic
- emotional, quiet, serious
- no text, no letters, no logos, no watermark
""".strip()
