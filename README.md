# The Badge Ritual — Design Your Door

> An interactive AI artwork inspired by Bob Dylan’s *Knockin’ on Heaven’s Door*.
>
> The project transforms a personal emotional burden — a “badge” — into a symbolic door, a spoken ritual, and an interactive threshold experience.

---

## 1. Project Overview

**The Badge Ritual** is an interactive generative AI artwork created for the **CSE 358 Introduction to Artificial Intelligence — Creative Project Assignment**.

The project is inspired by Bob Dylan’s 1973 song **“Knockin’ on Heaven’s Door”**, written for Sam Peckinpah’s film *Pat Garrett & Billy the Kid*. In the original scene, the dying sheriff carries the image of a badge, a weapon, and a final threshold. This project reinterprets that symbolic moment as a personal digital ritual: the user writes about an emotional burden they have been carrying, and the system transforms it into a visual, textual, and sonic experience.

The artwork is not designed as a therapy tool, productivity app, chatbot, or technical demo. It is designed as a **symbolic threshold experience**. The user enters three personal reflections:

1. What badge they have been carrying.
2. When they first started carrying it.
3. What it has cost them.

The system then generates:

* a symbolic title for the badge,
* a short historical echo connected to Dylan’s world,
* a custom AI-generated door image,
* a spoken ritual narration,
* an interactive badge-release moment,
* a knock interaction,
* and a final door response.

The central metaphor is simple: **everyone knocks on heaven’s door in their own way.** In this project, the door is not something that gives a direct answer. It is a threshold that allows the user to face what they have carried and decide what they are ready to leave behind.

---

## 2. Artistic Statement

This project takes the badge from Dylan’s song and turns it into a personal symbol. In *Knockin’ on Heaven’s Door*, the badge represents duty, identity, violence, exhaustion, and the burden of a role that can no longer be carried. In **The Badge Ritual**, the badge becomes whatever the user has been wearing in their own life: pride, fear, silence, perfectionism, anger, control, guilt, or a false version of strength.

The door represents a threshold between the old self and the next self. It does not promise healing, salvation, or a simple solution. Instead, it creates a ritual space where the user can name the burden, see it transformed into symbolic imagery, hear it reflected back in a human-like voice, release it onto the threshold, and knock.

The artwork combines **AI-generated language, AI-generated imagery, AI-generated speech, and original interactive code**. AI is used not as a replacement for authorship, but as a collaborator and mirror. The human provides the emotional material and artistic direction; AI transforms that material into symbolic forms; the interface turns the result into an experience.

---

## 3. Historical and Cultural Context

Bob Dylan wrote *Knockin’ on Heaven’s Door* for the 1973 Western film *Pat Garrett & Billy the Kid*. The song appears in a scene of death, farewell, and surrender. Although it was written for a specific cinematic moment, it became universal because its language is simple, symbolic, and emotionally open.

The song also belongs to a larger cultural atmosphere of the early 1970s: the Vietnam War, anti-war feeling, distrust of authority, the decline of heroic myths, and the questioning of violence, masculinity, and duty. The “badge” and “gun” in the song are not only physical objects; they are symbols of roles, systems, and burdens that become too heavy to carry.

This project carries that context into its structure. The user’s “badge” is treated as a role or burden. The AI-generated door becomes the threshold. The spoken narration becomes a ritual of farewell. The knock becomes a symbolic act of transition.

The historical context is not added only as background information. It shapes the project’s emotional grammar:

* the badge as duty and burden,
* the door as death, transition, and meaning,
* the Western atmosphere as visual memory,
* the ritual voice as farewell,
* the knock as the final action before crossing a threshold.

---

## 4. Core User Experience

The application follows a ritual-like flow:

### Step 1 — The User Names the Badge

The user writes what emotional burden or identity they have been carrying.

Example:

> “I always act strong because I am afraid people will see that I am tired.”

### Step 2 — The User Explains Its Origin

The user writes when or why they first started carrying this badge.

### Step 3 — The User Names Its Cost

The user reflects on what this badge has taken from them.

### Step 4 — AI Generates the Ritual

The backend sends the user’s input to the language model. The model returns structured JSON containing symbolic text, visual direction, materials, atmosphere, and narration.

### Step 5 — AI Generates the Door Image

The image generation service creates a symbolic door based on the user’s burden and the selected materials.

### Step 6 — AI Generates the Spoken Narration

The TTS service turns the generated ritual text into a spoken audio narration.

### Step 7 — The User Releases the Badge

On the result screen, a badge appears as a separate UI element over the door. The user clicks the release button and the badge falls from the door to the threshold.

### Step 8 — The User Knocks

After releasing the badge, the user approaches the knocker and knocks twice. The door slightly opens and the final symbolic response appears.

---

## 5. AI Techniques Used

This project uses multiple distinct generative AI techniques, satisfying the assignment requirement that at least two different AI techniques must be integrated into the work.

### 5.1 Large Language Model — Ritual Generation

The first AI technique is an LLM-based symbolic writing system. The model receives the user’s three inputs and generates a structured ritual response.

The LLM generates:

* `badgeTitle`
* `historicalEcho`
* `releaseText`
* `imagePrompt`
* `ttsText`
* `doorGuidance`
* `badgePlacementGuidance`
* `afterBadgeGuidance`
* `knockGuidance`
* `doorResponseGuidance`
* material and atmosphere fields

The language model is constrained by a strict JSON schema so that the frontend can reliably render the result.

### 5.2 Text-to-Image Generation — Door Artwork

The second AI technique is text-to-image generation. The project uses the generated image prompt to create a symbolic door that visually represents the user’s emotional burden.

The prompt includes:

* door material,
* threshold material,
* lighting style,
* atmosphere,
* symbolic meaning,
* cinematic composition rules,
* and restrictions to keep the badge out of the generated image.

The badge is intentionally not generated inside the image. It is rendered separately in the frontend so that the user can interact with it.

### 5.3 Text-to-Speech Generation — Spoken Ritual

The third AI technique is AI-generated speech. The generated `ttsText` is converted into a spoken narration. The voice is intended to feel calm, human, grounded, and emotionally close.

This gives the project a stronger ritual feeling. The artwork is not only read; it is heard.

### 5.4 Procedural Ambient Soundscape — Original Code-Based Audio Layer

In addition to AI-generated speech, the frontend uses a Web Audio API soundscape system. It creates atmospheric background sound based on the selected door material.

For example:

* old wood creates warmer, dusty tones,
* iron creates darker metallic ambience,
* glass or mirror doors create colder, more fragile tones,
* stone creates heavier and lower sound textures.

This soundscape is generated through original code and supports the emotional atmosphere of the ritual.

---

## 6. Technical Architecture

The project is built as a full-stack web application.

```text
The Badge Ritual
│
├── frontend/              # React application
│   ├── src/
│   │   ├── scenes/         # Main visual scenes
│   │   ├── services/       # API and ambient sound services
│   │   └── assets/         # Static frontend assets
│   └── package.json
│
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── prompts/        # Prompt engineering files
│   │   ├── services/       # LLM, image, and TTS services
│   │   └── routes/         # API endpoints
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

### 6.1 Frontend

The frontend is built with **React** and **Vite**.

Main frontend responsibilities:

* collect user input,
* call the backend API,
* show loading states,
* render the generated door image,
* display the generated ritual text,
* play narration audio,
* generate ambient soundscape,
* animate the badge release,
* handle the knock interaction,
* reveal the final door response.

### 6.2 Backend

The backend is built with **FastAPI**.

Main backend responsibilities:

* receive user ritual input,
* generate structured ritual JSON with an LLM,
* generate the image prompt,
* call the image generation service,
* call the text-to-speech service,
* return all generated outputs to the frontend.

### 6.3 Main Data Flow

```text
User Input
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
LLM Ritual Generation
   ↓
Image Prompt + TTS Text + Symbolic Guidance
   ↓
Text-to-Image Service + Text-to-Speech Service
   ↓
Generated Door Image + Audio Narration + Ritual JSON
   ↓
Interactive Result Scene
   ↓
Badge Release + Knock + Final Door Response
```

---

## 7. Installation and Setup

### 7.1 Requirements

Before running the project, install:

* Python 3.11+
* Node.js 18+
* npm
* Git
* OpenAI API key

Optional depending on the selected provider:

* Gemini API key

---

## 8. Backend Setup

Open a terminal and go to the backend folder:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```bash
cp .env.example .env
```

Then fill in the required API keys.

Example `.env` structure:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=verse

LLM_PROVIDER=openai
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## 9. Frontend Setup

Open a second terminal and go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

## 10. Example Input

The following example can be used to test the project:

### Badge

```text
I always act strong because I am afraid people will see that I am tired.
```

### Origin

```text
I started carrying this badge when I learned that showing weakness could make people leave or judge me.
```

### Cost

```text
It cost me honesty, rest, and the ability to ask for help when I needed it.
```

---

## 11. Example Output

A typical generated output includes:

* a symbolic badge title,
* a short historical echo connected to Dylan’s world,
* a release text,
* a generated door image,
* a spoken narration,
* material choices such as old wood, iron, glass, stone, or brass,
* and a final door response after the user knocks.

Example symbolic result:

```text
Badge Title: The Badge of Unbroken Strength
Historical Echo: Like the dying sheriff in Dylan’s song, this badge carries the weight of a role that once protected you but now asks to be laid down.
Release Text: You do not have to prove your strength by hiding your exhaustion.
```

---

## 12. Screenshots and Demo Evidence

The project includes screenshots that demonstrate the full ritual flow, from the first screen to the final door response.

### 1. Opening Screen

The user first enters the ritual space and is invited to begin.

![Opening Screen](screenshots/opening-screen.png)

### 2. Badge Input Screen

The user names the emotional badge they are still carrying.

![Badge Input Screen](screenshots/badge-input-screen.png)

### 3. Badge Origin and Cost Screen

The user explains when they first started carrying the badge and what it has cost them.

![Badge Origin and Cost Screen](screenshots/badge-origin-cost-screen.png)

### 4. Ritual Generation Loading Screen

The system processes the user’s words and begins forming the symbolic threshold.

![Ritual Generation Loading Screen](screenshots/ritual-loading-screen.png)

### 5. Generated Ritual Result

The project displays the generated badge title, symbolic door image, voice narration, badge text, door character, historical echo, and release text.

![Generated Ritual Result](screenshots/generated-ritual-result.png)

### 6. Historical Echo and Release Text

This screen shows the historical echo connected to Dylan’s 1973 context and the generated release text.

![Historical Echo and Release Text](screenshots/historical-echo-release-text.png)

### 7. Badge Placement Screen

The user prepares to place the badge before the door.

![Badge Placement Screen](screenshots/badge-placement-screen.png)

### 8. Badge Released Screen

The badge is placed at the threshold, visually showing that the burden is no longer carried in the same way.

![Badge Released Screen](screenshots/badge-released-screen.png)

### 9. Knock Interaction Screen

The user approaches the knocker and knocks twice to continue the ritual.

![Knock Interaction Screen](screenshots/knock-interaction-screen.png)

### 10. Final Door Response

The door opens slightly and gives the final symbolic response.

![Final Door Response](screenshots/final-door-response.png)

## 13. Original Code Contributions

This project includes original code for:

* frontend scene design,
* ritual interaction flow,
* badge release animation,
* knock interaction,
* custom audio player,
* procedural ambient soundscape generation,
* backend API structure,
* prompt engineering,
* LLM schema handling,
* image prompt strengthening,
* TTS generation pipeline,
* and full-stack integration.

The project is not a no-code AI output. It is a working application that integrates multiple AI services with a custom interactive experience.

---

## 14. Academic Integrity and AI Transparency

Generative AI tools are intentionally used in this project, as required by the assignment. However, the project’s concept, structure, code integration, artistic direction, and final curation are human-authored.

AI is used for:

* symbolic ritual text generation,
* door image generation,
* spoken narration generation.

Original human work includes:

* project concept,
* interaction design,
* prompt engineering direction,
* frontend and backend implementation,
* material system,
* badge-release ritual logic,
* soundscape design,
* README and manifesto writing,
* final artistic interpretation.

All API keys must remain private and must not be committed to GitHub. The `.env` file is excluded from the repository. A `.env.example` file is provided for setup instructions.

---

## 15. Technologies Used

### Frontend

* React
* Vite
* JavaScript
* CSS
* Web Audio API

### Backend

* Python
* FastAPI
* Uvicorn
* OpenAI API
* optional Gemini API support

### AI Techniques

* Large Language Model generation
* Text-to-image generation
* Text-to-speech generation

---

## 16. Project Evaluation Alignment

This project is designed according to the assignment rubric.

### Technical Depth

* Uses multiple AI techniques.
* Integrates AI outputs into a working pipeline.
* Includes original full-stack code.
* Uses structured JSON generation and frontend rendering.
* Includes procedural audio and interactive animation.

### Artistic Originality

* Reinterprets Dylan’s badge and door symbols as a personal digital ritual.
* Uses a coherent visual, textual, and sonic atmosphere.
* Turns user input into a unique symbolic artwork.

### Philosophical Engagement

* Connects to Dylan’s song, the 1973 film context, farewell, death, duty, and burden.
* Explores what it means to carry and release a role.
* Uses the door as a threshold between identity, memory, and transformation.

### Presentation and Craft

* Provides a complete interactive demo.
* Includes frontend, backend, AI generation, audio, and visual output.
* Designed to be demonstrated live and explained clearly.

---

## 17. How to Present the Demo

A recommended demo flow:

1. Briefly explain Dylan’s song and the badge/door metaphor.
2. Show the input screen.
3. Enter a sample personal badge.
4. Generate the ritual.
5. Show the generated door image.
6. Play the spoken narration.
7. Release the badge from the door.
8. Knock on the door.
9. Show the final door response.
10. Explain how the AI techniques interact behind the scenes.

---

## 18. Repository Notes

Before submission, check that:

* `.env` is not committed,
* `.env.example` exists,
* `requirements.txt` is updated,
* frontend dependencies are listed in `package.json`,
* screenshots are included,
* the project runs locally,
* the README is complete,
* the Artist’s Manifesto is included separately.

---

## 19. Author

**Batuhan Erdem**
Computer Engineering Student
CSE 358 — Introduction to Artificial Intelligence

---

## 20. Final Note

*The Badge Ritual* is a digital artwork about the moment when a person realizes that something once worn for protection has become too heavy to carry. The project does not ask what is behind the door. It asks what the user is ready to leave at the threshold before knocking.
