import aiormq
from consumer import handlers
from config import settings


async def consumer_subscriptions():
    connection = await aiormq.connect(settings.AMQP_URI)
    channel = await connection.channel()
    chat_message_queue__declared = await channel.queue_declare(
        f"{settings.UNIQUE_PREFIX}:external__main:chat_message",
        durable=False,
    )
    await channel.basic_consume(
        chat_message_queue__declared.queue,
        handlers.chat_message,
        no_ack=False,
    )
