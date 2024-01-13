import aiormq


from consumer import methods
from config import se


async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()

    pow_chat_message_queue__declared = await channel.queue_declare(
        f"{UNIQUE_PREFIX}:internal__worker:pow_chat_message", durable=False
    )

    # no_ack=False - поведение по умолчанию, отвечаем принудительно в самом обработчике по мере выполенения (предпочитаемый вариант)
    await channel.basic_consume(
        pow_chat_message_queue__declared.queue, methods.pow_chat_message, no_ack=False
    )
