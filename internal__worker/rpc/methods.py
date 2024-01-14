import json
import aiormq
from aiormq.abc import DeliveredMessage

from consumer import helpers


async def pow_chat_message_rpc(message: DeliveredMessage):
    incoming_message_dict = json.loads(message.body)

    incoming_message = incoming_message_dict["message"]
    hash_result, calculate_elapsed_time = await helpers.PoW(
        incoming_message
    ).calculate()
    outcoming_message_dict = {}
    outcoming_message_dict["username"] = "internal_worker"
    outcoming_message_dict["message"] = (
        f"POW RPC {incoming_message} "
        + f"hash:{hash_result} elapsed time:{calculate_elapsed_time}"
    )
    outcoming_message_dict["source"] = "internal_worker"

    outcoming_message_bytes = json.dumps(outcoming_message_dict).encode()

    await message.channel.basic_publish(
        outcoming_message_bytes,
        routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),
    )
    await message.channel.basic_ack(message.delivery.delivery_tag)
