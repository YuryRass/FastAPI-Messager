import json
from aiormq.abc import DeliveredMessage
from pydantic import BaseModel, Field, ValidationError


class Message(BaseModel):
    username: str = Field()
    message: str = Field()


def validate_request_schema():
    def wrap(func):
        async def wrapped(message: DeliveredMessage):
            await message.channel.basic_ack(message.delivery.delivery_tag)

            try:
                json_data = json.loads(message.body)
                validated_data = Message(**json_data).model_dump()
                await func(validated_data)
            except (ValidationError, Exception) as e:
                print(f"~ ERROR REQUEST: body={message.body} error={e}")

        return wrapped

    return wrap
