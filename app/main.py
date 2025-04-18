from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from app.api.mainRoute import api_router
from app.core.config import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)