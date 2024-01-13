import aiormq
import json
from config import settings


async def send_message_to_internal_messager(outcoming_message: dict):
    outcoming_message.update({"source": "external__main"})
    outcoming_message_bytes = json.dumps(outcoming_message).encode()
    connection = await aiormq.connect(settings.AMQP_URI)
    channel = await connection.channel()
    await channel.basic_publish(
        outcoming_message_bytes,
        routing_key=f"{settings.UNIQUE_PREFIX}:internal__messager:chat_message",
    )
    await connection.close()
