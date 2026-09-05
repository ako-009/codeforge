# app/main.py
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="CodeForge",
    description="Agentic code synthesis with sandboxed execution and self-repair",
    version="1.0.0"
)

app.include_router(router)