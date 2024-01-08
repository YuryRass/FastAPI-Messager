from fastapi import FastAPI

from pages.router import router as page_router
from chat.router import router as chat_router

app = FastAPI()

app.include_router(page_router)
app.include_router(chat_router)
