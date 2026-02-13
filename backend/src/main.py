from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from src.api.v1.router import api_router

app = FastAPI(
    title="Akinator Clone API",
    description="Базовый HTTP-сервер с заглушками",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)