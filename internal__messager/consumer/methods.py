import json
from aiormq.abc import DeliveredMessage

from producer import methods as producer_methods


async def simple_message(message: DeliveredMessage):
    print(f"simple_message :: body is {message.body!r}")


async def simple_message_with_ack(message: DeliveredMessage):
    print(f"simple_message_with_ack :: body is: {message.body!r}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_message(message: DeliveredMessage):
    incoming_message: dict = json.loads(message.body)
    incoming_message: str = incoming_message["message"]

    if (
        incoming_message.endswith('!pow')
        and incoming_message["source"] == "external__main"
    ):
        outcoming_message: dict = {}
        outcoming_message["username"] = "internal_messager"
        outcoming_message["message"] = incoming_message
        await producer_methods.send_pow_message_to_internal_worker(
            outcoming_message
        )
        await message.channel.basic_ack(message.delivery.delivery_tag)
    else:
        if incoming_message["source"] == "external__main":
            outcoming_message = incoming_message[::-1]
        elif incoming_message["source"] == "internal__worker":
            outcoming_message = incoming_message
        outcoming_message: dict = {}
        outcoming_message["username"] = "internal_messager"
        outcoming_message["message"] = outcoming_message
        await producer_methods.send_message_to_external_main(outcoming_message)
        await message.channel.basic_ack(message.delivery.delivery_tag)
