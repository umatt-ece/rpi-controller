import asyncio
import json

from database import DataStore, LiveData as lD, StoredData as sD


class ClientManager:

    def __init__(self):
        self._data_store = DataStore()
        self._clients = {}

    async def _send_text(self, client_id, msg: str):
        try:
            await self._clients[client_id].send_text(msg)
        except Exception as e:
            print(f'Exception: {e}')

    async def add_client(self, client_id, websocket):
        print('adding new client...')
        self._clients[client_id] = websocket

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
        if client_id in self._clients:
            del self._clients[client_id]

    async def broadcast(self, msg: dict):
        for client_id, client in list(self._clients.items()):
            await self._send_text(client_id, json.dumps(msg, default=str))

    async def run(self):
        print('starting up Client Manager')

        while True:
            try:
                msg = {
                    'type': 'live_data',
                    'data': self._data_store.get_many(list(lD))
                }
                await self.broadcast(msg)
                await asyncio.sleep(INTERVAL)
            except Exception as e:
                print(f'Exception: {e}')


INTERVAL = 0.1  # seconds
