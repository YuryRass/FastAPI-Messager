import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from chat.router import router as chat_router
from cron import one_minute_message
from pages.router import router as page_router
from consumer.subscriptions import consumer_subscriptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    one_minute_message.start()
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())
    yield
    one_minute_message.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(page_router)
app.include_router(chat_router)
