from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.types import Scope, Receive, Send
from starlette.websockets import WebSocket

router = APIRouter()


# TODO: sort out this file lol... it's a mess

@router.websocket_route('/ws')
class WebsocketRoutes(WebSocketEndpoint):
    def __init__(self, scope: Scope, receive: Receive, send: Send):
        super().__init__(scope, receive, send)

        self._client_id = None
        # self._client_manager = client_manager # TODO: dependency inject the ClientManager in here

    async def on_connect(self, websocket):
        """
        handle new connection
        """
        # self._client_id = str(uuid.uuid4())  # TODO: uuids???
        await websocket.accept()
        await self._client_manager.add_client(self._client_id, websocket)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        """
        disconnect client
        """
        if self._client_id is None:
            raise RuntimeError("on_disconnect() called without a valid client_id")
        await self._client_manager.remove_client(self._client_id)

    # async def on_receive(self, _websocket: WebSocket, msg: Any):
    #     """
    #     handle incoming message
    #      - `msg` is forwarded straight to `broadcast_message`
    #     """
    #     if self._client_id is None:
    #         raise RuntimeError("WebSocketRoute.on_receive() called without a valid client_id")
    #     if not isinstance(msg, str):
    #         raise ValueError(f"WebSocketRoute.on_receive() passed unhandleable data: {msg}")
    #     await self._client_manager.broadcast_message(self._client_id, msg)
