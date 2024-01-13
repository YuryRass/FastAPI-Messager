import aiormq
import json
from config import settings


async def send_message_to_external_main(outcoming_message: dict):
    outcoming_message.update({"source": "internal__messager"})
    outcoming_message_bytes = json.dumps(outcoming_message).encode()
    connection = await aiormq.connect(settings.AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(
        outcoming_message_bytes,
        routing_key=f"{settings.UNIQUE_PREFIX}:external__main:chat_message",
    )
    await connection.close()


async def send_pow_message_to_internal_worker(outcoming_message: dict):
    outcoming_message.update({"source": "internal__messager"})
    outcoming_message_bytes = json.dumps(outcoming_message).encode()
    connection = await aiormq.connect(settings.AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(
        outcoming_message_bytes,
        routing_key=f"{settings.UNIQUE_PREFIX}:internal__worker:pow_chat_message",
    )
    await connection.close()
