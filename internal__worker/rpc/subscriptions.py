import aiormq

from consumer import methods
from config import settings
from rpc import methods


async def rpc_subscriptions():
    connection = await aiormq.connect(settings.AMQP_URI)
    channel = await connection.channel()

    pow_chat_message_rpc_queue__declared = await channel.queue_declare(
        f"{settings.UNIQUE_PREFIX}:internal_worker:pow_chat_message_rpc",
        durable=False,
    )

    await channel.basic_consume(
        pow_chat_message_rpc_queue__declared.queue,
        methods.pow_chat_message_rpc,
        no_ack=False,
    )
