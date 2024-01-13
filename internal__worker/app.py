import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from consumer.subscriptions import consumer_subscriptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())
    yield


app = FastAPI(lifespan=lifespan)
