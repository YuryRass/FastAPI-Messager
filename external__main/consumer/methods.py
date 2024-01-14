from channel_box import ChannelBox


async def chat_message(validated_data: dict):
    await ChannelBox.group_send(
        "MyChat",
        {
            "username": validated_data["username"],
            "message": validated_data["message"],
        },
    )
