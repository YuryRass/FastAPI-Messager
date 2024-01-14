from config import settings
from consumer.helpers import MyRpcClient
from producer import methods as producer_methods


async def chat_message(validated_data: dict):
    incoming_message: str = validated_data["message"]

    if (
        len(incoming_message) > 4
        and incoming_message.endswith("!pow")
        and validated_data["source"] == "external__main"
    ):
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message[:-4]
        await producer_methods.send_pow_message_to_internal_worker(
            outcoming_message_dict
        )
    elif len(incoming_message) > 4 and incoming_message.endswith("!rpc"):
        outcoming_message_dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = incoming_message[:-4]
        fibonacci_rpc = await MyRpcClient().connect()
        message_dict = await fibonacci_rpc.call(
            outcoming_message_dict,
            f"{settings.UNIQUE_PREFIX}:internal_worker:pow_chat_message_rpc",
        )
        await producer_methods.send_message_to_external_main(message_dict)
    else:
        if validated_data["source"] == "external__main":
            outcoming_message = incoming_message[::-1]
        elif validated_data["source"] == "internal__worker":
            outcoming_message = incoming_message
        outcoming_message_dict: dict = {}
        outcoming_message_dict["username"] = "internal_messager"
        outcoming_message_dict["message"] = outcoming_message
        await producer_methods.send_message_to_external_main(
            outcoming_message_dict,
        )
