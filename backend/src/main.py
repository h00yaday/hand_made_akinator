from fastapi import FastAPI
from src.api.v1.endpoints import game

app = FastAPI(
    title="Akinator Clone API",
    description="Базовый HTTP-сервер с заглушками",
    version="1.0.0",
    docs_url="/docs" # Swagger по умолчанию тут
)

app.include_router(game.router, prefix="/api/v1/game", tags=["Game"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)