from fastapi import FastAPI

from src.config import config
from src.api.routes.ask import router as ask_router

app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)


@app.get("/health")
def health_check():
    return {
        "App Name": config.APP_NAME,
        "App Version": config.APP_VERSION,
        "Status": "ok",
        "Model Name": config.GENERATION_MODEL_NAME,
    }

app.include_router(ask_router)