import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from consumer.subscriptions import consumer_subscriptions
from rpc.subscriptions import rpc_subscriptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())
    loop.create_task(rpc_subscriptions())
    yield


app = FastAPI(lifespan=lifespan)
