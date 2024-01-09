from channel_box import Channel, ChannelBox
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ConnectionManager:
    channels: dict[WebSocket, Channel] = {}

    async def on_connect(self, websocket: WebSocket):
        group_name = websocket.query_params.get(
            "group_name"
        )  # group name */ws?group_name=MyChat
        if group_name:
            channel = Channel(
                websocket,
                expires=60 * 60,
                encoding="json",
            )  # define user channel
            self.channels[websocket] = channel
            channel = await ChannelBox.channel_add(
                group_name,
                channel,
            )  # add user channel to named group
        await websocket.accept()

    async def on_send(
        self,
        data: dict[str, str],
        group_name: str | None,
    ):
        message = data["message"]
        username = data["username"]

        if message.strip():
            payload = {
                "username": username,
                "message": message,
            }
            if group_name:
                await ChannelBox.group_send(
                    group_name, payload
                )  # send to all users channels


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    group_name: str,
):
    await manager.on_connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.on_send(data, group_name)
    except WebSocketDisconnect:
        await ChannelBox.channel_remove(
            group_name,
            manager.channels[websocket],
        )
        await ChannelBox.group_send(
            group_name,
            {
                "username": f"user #{client_id}",
                "message": "left the chat",
            },
        )
