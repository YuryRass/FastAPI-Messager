import json
from aiormq.abc import DeliveredMessage


def show(message: bytes):
    try:
        return json.loads(message)
    except ValueError:
        return repr(message.decode())


async def simple_message(message: DeliveredMessage):
    print(f"simple_message :: Simple message body is {show(message.body)}")


async def simple_message_with_ack(message: DeliveredMessage):
    print(f"simple_message_with_ack :: Simple message body is: {show(message.body)}")
    await message.channel.basic_ack(message.delivery.delivery_tag)
