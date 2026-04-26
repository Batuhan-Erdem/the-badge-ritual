# backend/app/prompts/image_prompt.py

def _infer_material_and_mood(text: str) -> tuple[str, str, str]:
    """
    Very light symbolic mapping so the door can visually change
    depending on the emotional burden.
    Returns: (door_material, atmosphere, knocker_material)
    """
    content = (text or "").lower()

    hard_words = [
        "anger", "angry", "rage", "control", "power", "armor", "mask",
        "strong", "strength", "hard", "strict", "cold",
        "öfke", "kontrol", "güç", "maske", "sert", "katı", "soğuk"
    ]
    sad_words = [
        "sad", "grief", "loss", "lonely", "loneliness", "silence", "tired",
        "sorrow", "exhausted", "broken",
        "üzgün", "yas", "kayıp", "yalnız", "sessizlik", "yorgun", "kırık"
    ]
    guilt_words = [
        "guilt", "shame", "regret", "burden", "fear",
        "suçluluk", "utanç", "pişmanlık", "yük", "korku"
    ]

    if any(word in content for word in hard_words):
        return (
            "heavy dark wood reinforced with aged iron details",
            "tense, still, solemn, emotionally weighty",
            "dark iron"
        )

    if any(word in content for word in sad_words):
        return (
            "weathered old wood with softened worn edges",
            "quiet, melancholic, dim, intimate",
            "aged bronze"
        )

    if any(word in content for word in guilt_words):
        return (
            "old wood with worn grain and tarnished metal traces",
            "heavy, reflective, shadowy, remorseful",
            "tarnished brass"
        )

    return (
        "aged wooden door with subtle worn texture",
        "quiet, cinematic, symbolic, serious",
        "aged bronze"
    )


def build_image_prompt(badge_title: str = "", badge_text: str = "") -> str:
    """
    Main image prompt builder.
    This is the function we want the app to use.
    """
    symbolic_input = f"{badge_title} {badge_text}".strip()
    door_material, atmosphere, knocker_material = _infer_material_and_mood(symbolic_input)

    return f"""
Create a symbolic, cinematic digital artwork of a single door that represents a personal threshold.

VERY IMPORTANT COMPOSITION RULES:
- The door must be the clear main subject.
- Show the FULL door from top to bottom, completely visible.
- The door must be large and dominant, filling about 80% to 90% of the frame height.
- The door must look human-sized and imposing, never tiny, distant, miniature, or doll-like.
- The camera must face the door almost straight-on.
- The door must be centered in the composition.
- The entire doorframe and threshold should be visible.
- The image must feel like a serious ritual scene, not a landscape shot.
- Do NOT place the door far away in the background.
- Do NOT make the door small in a large empty environment.
- Do NOT crop away important parts of the door.
- The scene should visually focus on the door itself.

DOOR DETAILS:
- The door is made of {door_material}.
- The door has a visible circular knocker made of {knocker_material}.
- The knocker should sit in the upper-middle area of the door and be clearly visible.
- A small sheriff-style metal badge lies on the ground at the threshold, beneath the door.
- The badge must be much smaller than the door and should not dominate the image.

ATMOSPHERE:
- The image should feel {atmosphere}.
- Twilight or low warm light.
- Subtle 1970s folk-western cinematic feeling.
- Symbolic, melancholic, emotional, quiet.
- Warm amber, brown, umber, smoky gold, and muted shadow tones.
- Painterly but believable.
- Serious and elegant.

SYMBOLIC CONTEXT:
- The door represents a threshold that the user can only approach after laying down an emotional burden.
- The badge represents a role, burden, mask, fear, or identity being left behind.
- The scene should visually feel like “leaving something at the threshold before knocking.”

USER SYMBOLIC BURDEN:
- Badge title: {badge_title if badge_title else "Unnamed burden"}
- Badge meaning: {badge_text if badge_text else "A burden being laid down"}

NEGATIVE INSTRUCTIONS:
- no text
- no captions
- no subtitles
- no letters
- no watermark
- no logo
- no extra people
- no crowd
- no tiny door
- no distant door
- no miniature doorway
- no exaggerated empty foreground

The final image must look like a powerful, full, emotionally rich ritual door scene with the complete door clearly visible.
""".strip()


# Extra aliases for compatibility with different import styles
def get_image_prompt(badge_title: str = "", badge_text: str = "") -> str:
    return build_image_prompt(badge_title, badge_text)


def create_image_prompt(badge_title: str = "", badge_text: str = "") -> str:
    return build_image_prompt(badge_title, badge_text)

def strengthen_image_prompt(base_prompt: str) -> str:
    return f"""
{base_prompt}

VERY IMPORTANT COMPOSITION RULES:
- The image must show ONE large, full, human-sized door.
- The complete door must be visible from top to bottom.
- The door must fill about 80% to 90% of the image height.
- The door must be large, dominant, close to the viewer, and emotionally imposing.
- Do not make the door small, distant, miniature, doll-like, or lost in a large landscape.
- The camera must face the door almost straight-on.
- The door must be centered in the composition.
- The full doorframe and threshold must be visible.
- The scene must visually focus on the door itself, not on the background.
- Avoid large empty areas above, below, or around the door.
- Avoid large black empty space under the threshold.

MANDATORY VISUAL REQUIREMENTS:
- symbolic digital artwork
- one central door as the main subject
- the door material must be visually clear
- a visible circular door knocker must be placed clearly on the upper-middle center of the door
- a small symbolic metal badge must rest on the ground near the threshold
- the badge should feel like a burden that has been put down
- the badge must be much smaller than the door and should not dominate the image
- the scene must look like a finished cinematic artwork, not a plain object render

FRAMING REQUIREMENTS:
- square composition
- centered frontal door composition
- threshold area must be visible near the lower edge
- badge near the lower part of the image
- door knocker visible around the upper-middle part of the door
- keep the door centered and frontal enough for an interactive door-opening effect

ATMOSPHERE REQUIREMENTS:
- dusty western atmosphere
- twilight lighting
- muted 1970s cinematic mood
- melancholic folk feeling
- quiet threshold moment
- warm amber, dark brown, faded beige, worn metal, and shadow tones
- painterly but realistic
- emotional, serious, restrained, and poetic

NEGATIVE INSTRUCTIONS:
- no people
- no readable text
- no letters
- no captions
- no logos
- no watermark
- no tiny door
- no distant door
- no miniature doorway
- no exaggerated empty foreground
- no huge empty background

The final image must look like a powerful, full, emotionally rich ritual door scene with the complete door clearly visible.
""".strip()