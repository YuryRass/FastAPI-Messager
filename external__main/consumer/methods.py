import json
from aiormq.abc import DeliveredMessage
from channel_box import ChannelBox


async def chat_message(message: DeliveredMessage):
    incoming_message_dict = json.loads(message.body)
    await ChannelBox.group_send(
        "MyChat",
        {
            "username": incoming_message_dict["username"],
            "message": incoming_message_dict["message"],
        },
    )
    await message.channel.basic_ack(message.delivery.delivery_tag)
