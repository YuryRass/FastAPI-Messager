import json
from aiormq.abc import DeliveredMessage

from producer import methods as producer_methods


async def simple_message(message: DeliveredMessage):
    print(f"simple_message :: body is {message.body!r}")


async def simple_message_with_ack(message: DeliveredMessage):
    print(f"simple_message_with_ack :: body is: {message.body!r}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_message(message: DeliveredMessage):
    incoming_message_dict = json.loads(message.body)
    message_source: str = incoming_message_dict["source"]
    incoming_message: str = incoming_message_dict["message"]

    if (
        "!pow" in incoming_message
        and message_source == "external__main"
    ):
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message[:-4]
        await producer_methods.send_pow_message_to_internal_worker(
            outcoming_message_dict
        )
        await message.channel.basic_ack(message.delivery.delivery_tag)
    else:
        if message_source == "external__main":
            outcoming_message = incoming_message[::-1]
        elif message_source == "internal__worker":
            outcoming_message = incoming_message
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = outcoming_message
        await producer_methods.send_message_to_external_main(outcoming_message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)
