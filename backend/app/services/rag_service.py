from pathlib import Path


KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"


def read_markdown_file(file_name: str) -> str:
    """
    Reads a markdown file from the knowledge_base directory.
    Returns an empty string if the file does not exist.
    """
    file_path = KNOWLEDGE_BASE_DIR / file_name

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8")


def get_ritual_context() -> str:
    """
    Collects curated historical, symbolic, and tonal context
    for The Badge Ritual project.

    This context will later be injected into the LLM prompt.
    """
    files = [
        "song_context.md",
        "historical_context.md",
        "symbolic_context.md",
        "tone_guide.md",
    ]

    context_parts = []

    for file_name in files:
        content = read_markdown_file(file_name)

        if content.strip():
            context_parts.append(content.strip())

    return "\n\n---\n\n".join(context_parts)


def build_user_context(badge: str, origin: str, cost: str) -> str:
    """
    Builds a clean user-specific context block.
    This separates the user's personal input from the historical RAG context.
    """
    return f"""
User's Badge:
{badge}

When the user first started carrying it:
{origin}

What it has cost the user:
{cost}
""".strip()


def build_full_context(badge: str, origin: str, cost: str) -> str:
    """
    Combines curated project knowledge with the user's personal ritual input.
    """
    ritual_context = get_ritual_context()
    user_context = build_user_context(badge, origin, cost)

    return f"""
PROJECT KNOWLEDGE BASE:
{ritual_context}

USER RITUAL INPUT:
{user_context}
""".strip()

