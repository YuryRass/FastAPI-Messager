from consumer import schema
from consumer import methods


@schema.validate_request_schema()
async def pow_chat_message(validated_data):
    await methods.pow_chat_message(validated_data)
