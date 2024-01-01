import logging
import uuid

from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.types import Scope, Receive, Send
from starlette.websockets import WebSocket

websockets = APIRouter()


def inject_client_manager(logger: logging.Logger = None):
    """
    In order to avoid circular imports during initialization, the get_client_manager function must be imported later
    and called within this function.
    """
    from common.dependency_handler import get_client_manager
    return get_client_manager(logger=logger)


@websockets.websocket_route('/ws')
class WebsocketRoutes(WebSocketEndpoint):
    """

    """

    def __init__(self, scope: Scope, receive: Receive, send: Send, logger: logging.Logger = None):
        super().__init__(scope, receive, send)
        self._logger = logger or logging.getLogger("server")

        self._client_id = None
        self._client_manager = inject_client_manager()

    async def on_connect(self, websocket: WebSocket) -> None:
        """
        handle new connection
        """
        self._client_id = str(uuid.uuid4())  # Generate an unique identifier (UUID)
        self._logger.info(f"New WebSocket connected, assigning it ID: {self._client_id}")

        # Accept the connection and add it to the list of connected clients
        await websocket.accept()
        await self._client_manager.add_client(self._client_id, websocket)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
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
