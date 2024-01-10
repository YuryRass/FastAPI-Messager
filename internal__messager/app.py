import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from internal__messager.consumer.subscriptions import consumer_subscriptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())
    yield
    loop.close()


app = FastAPI(lifespan=lifespan)
