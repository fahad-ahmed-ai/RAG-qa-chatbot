from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from bot.routes import chat_router
from document.routes import knowledge_router


application = FastAPI(title="Q&A Bot Backend")


application.include_router(
    chat_router, prefix="/chat", tags=["Chat"]
)

application.include_router(
    knowledge_router, prefix="/knowledge", tags=["Knowledge Base"]
)

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

