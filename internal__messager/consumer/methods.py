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
    incoming_message = incoming_message_dict["message"]

    if len(incoming_message) > 5 and incoming_message[-4:] == "!pow":
        pass
    else:
        outcoming_message = incoming_message[::-1]

    outcoming_message_dict = {}
    outcoming_message_dict["username"] = "internal_messager"
    outcoming_message_dict["message"] = outcoming_message
    await producer_methods.send_message_to_external_main(outcoming_message_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)
