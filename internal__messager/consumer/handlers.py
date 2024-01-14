from consumer import schema
from consumer import methods


@schema.validate_request_schema()
async def chat_message(validated_data):
    await methods.chat_message(validated_data)
