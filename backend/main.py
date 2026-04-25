from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ritual_routes import router as ritual_router

app = FastAPI(
    title="The Badge Ritual API",
    description="Backend API for The Badge Ritual interactive AI artwork.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ritual_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "The Badge Ritual backend is running."
    }
