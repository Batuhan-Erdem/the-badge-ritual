def strengthen_image_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

Mandatory visual requirements:
- symbolic digital artwork
- one central door as the main subject
- the door material must be visually clear
- a visible door knocker must be placed on the door
- a small symbolic metal badge must rest on the ground near the threshold
- the badge should feel like a burden that has been put down
- the door should feel personal, heavy with meaning, and connected to the user's emotional burden
- the scene must look like a finished cinematic artwork, not a plain object render

Atmosphere requirements:
- dusty western atmosphere
- twilight lighting
- muted 1970s cinematic mood
- melancholic folk feeling
- quiet threshold moment
- warm amber, dark brown, faded beige, worn metal, and shadow tones
- painterly but realistic
- emotional, serious, restrained, and poetic
- subtle sense of silence after a long journey

Composition requirements:
- vertical or centered composition
- door occupies the emotional center of the image
- threshold area must be visible
- badge near the lower part of the image
- door knocker visible around the middle/upper part of the door
- no people
- no readable text
- no letters
- no logos
- no watermark
- no captions
""".strip()
