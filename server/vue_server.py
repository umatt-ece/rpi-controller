import logging
import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from server import ClientManager, WebsocketRoutes, SystemRoutes

logger = logging.getLogger("server")


def create_app() -> FastAPI:
    new_app = FastAPI()
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.include_router(SystemRoutes)
    new_app.add_websocket_route('/ws', WebsocketRoutes)
    new_app.mount("/", StaticFiles(directory="vue-app", html=True), name="VueJS App")
    return new_app


app = create_app()


@app.get("/")
async def vuejs_app():
    return FileResponse('vue-app/index.html', media_type='text/html')


@app.on_event('startup')
async def app_startup():
    logger.info("Starting Client Manager...")
    # client_manager = ClientManager()
    # asyncio.create_task(client_manager.run())


def start_vue_server(host: str = "localhost", port: int = 8577) -> None:
    logger.info(f"Starting Vue Server on '{host}:{port}'")
    uvicorn.run(app, host=host, port=port)
