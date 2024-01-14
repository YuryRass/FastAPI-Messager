from producer import methods as producer_methods
from consumer import helpers


async def pow_chat_message(validated_data: dict):
    incoming_message = validated_data["message"]
    hash_result, calculate_elapsed_time = await helpers.PoW(
        incoming_message
    ).calculate()

    outcoming_message_dict = {}
    outcoming_message_dict["username"] = "internal_messager"
    outcoming_message_dict["message"] = (
        f"POW {incoming_message} "
        + f"hash:{hash_result} elapsed time:{calculate_elapsed_time}"
    )
    await producer_methods.send_message_to_internal_messager(
        outcoming_message_dict,
    )
