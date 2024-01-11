import aiocron
from channel_box import ChannelBox


@aiocron.crontab("*/1 * * * *", start=False)
async def one_minute_message():
    await ChannelBox.group_send(
        group_name="MyChat",
        payload={"username": "CronTab", "message": "Hello world"},
    )
