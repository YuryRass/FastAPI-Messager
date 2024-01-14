import json
from aiormq.abc import DeliveredMessage

from config import settings
from consumer.helpers import FibonacciRpcClient
from producer import methods as producer_methods


async def simple_message(message: DeliveredMessage):
    print(f"simple_message :: body is {message.body!r}")


async def simple_message_with_ack(message: DeliveredMessage):
    print(f"simple_message_with_ack :: body is: {message.body!r}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def chat_message(message: DeliveredMessage):
    incoming_message_dict = json.loads(message.body)
    incoming_message: str = incoming_message_dict["message"]

    if (
        len(incoming_message) > 4
        and incoming_message.endswith("!pow")
        and incoming_message_dict["source"] == "external__main"
    ):
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message[:-4]
        await producer_methods.send_pow_message_to_internal_worker(
            outcoming_message_dict
        )
        await message.channel.basic_ack(message.delivery.delivery_tag)
    elif len(incoming_message) > 4 and incoming_message.endswith("!rpc"):
        outcoming_message_dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message[:-4]
        fibonacci_rpc = await FibonacciRpcClient().connect()
        message_dict = await fibonacci_rpc.call(
            outcoming_message_dict,
            f"{settings.UNIQUE_PREFIX}:internal_worker:pow_chat_message_rpc",
        )
        await producer_methods.send_message_to_external_main(message_dict)
        await message.channel.basic_ack(message.delivery.delivery_tag)
    else:
        if incoming_message_dict["source"] == "external__main":
            outcoming_message = incoming_message[::-1]
        elif incoming_message_dict["source"] == "internal__worker":
            outcoming_message = incoming_message
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = outcoming_message
        await producer_methods.send_message_to_external_main(
            outcoming_message_dict,
        )
        await message.channel.basic_ack(message.delivery.delivery_tag)
