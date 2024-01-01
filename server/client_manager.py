import logging
import asyncio
import json

INTERVAL = 0.5  # seconds


def inject_data_store(logger: logging.Logger = None):
    """
    In order to avoid circular imports during initialization, the get_data_store function must be imported later
    and called within this function.
    """
    from common.dependency_handler import get_data_store
    return get_data_store(logger=logger)


class ClientManager:

    def __init__(self, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger("server")

        self._data_store = inject_data_store()
        self._clients = {}

    async def _send_text(self, client_id, msg: str):
        """

        """
        try:
            await self._clients[client_id].send_text(msg)
        except Exception as e:
            self._logger.exception(e)  # Log exception but don't crash

    async def add_client(self, client_id: str, websocket) -> None:
        """

        """
        self._logger.info(f"New client added to list of clients with ID: {client_id}")

        # Add the new client to our list of clients
        self._clients[client_id] = websocket

        # Respond to newly connected client to let them know the connection was successful
        await websocket.send_json(
            {
                'type': 'CONNECTION_SUCCESSFUL',
                'data': {
                    'is_connected': True,
                    'client_id': client_id,
                    'no_of_active_connections': len(self._clients),
                }
            }
        )

    async def remove_client(self, client_id):
        """

        """
        if client_id in self._clients:
            del self._clients[client_id]

    async def broadcast(self, msg: dict):
        """

        """
        for client_id, client in list(self._clients.items()):
            await self._send_text(client_id, json.dumps(msg, default=str))

    async def run(self):
        """

        """
        self._logger.info(f"Client Manager's 'broadcast' thread started successfully")

        try:
            while True:  # Run this thread 'forever' (unless forcefully closed by the Operating System)

                # Construct broadcast message
                msg = {
                    'type': 'update',
                    'data': []
                }

                # Send message and wait for next interval
                await self.broadcast(msg)
                await asyncio.sleep(INTERVAL)

        except Exception as e:
            self._logger.exception(e)
            raise e
