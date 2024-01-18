import logging
import threading
import asyncio

import uvicorn
from fastapi_offline import FastAPIOffline
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from server import router, websockets

_logger = logging.getLogger("server")


def inject_logging_config() -> dict:
    """
    In order to avoid circular imports, the logging_config must be imported after initialization
    """
    from common import logging_config
    return logging_config


def inject_client_manager(logger: logging.Logger = None):
    """
    In order to avoid circular imports during initialization, the get_client_manager function must be imported later
    and called within this function.
    """
    from common.dependency_handler import get_client_manager
    return get_client_manager(logger=logger)


def create_app() -> FastAPIOffline:
    new_app = FastAPIOffline()
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.include_router(router)
    new_app.mount("/", StaticFiles(directory="server/vue-app", html=True), name="VueJS App")
    return new_app


app = create_app()


@app.get("/")
async def vuejs_app():
    return FileResponse('vue-app/index.html', media_type='text/html')


@app.on_event('startup')
async def app_startup():
    _logger.info("Starting Client Manager...")

    client_manager = inject_client_manager()

    # Due to the 'asynchronous' nature of the `client_manager`, the run() method needs to be called using `asyncio.run`
    # In order for it to execute in a separate thread.
    client_manager_broadcast_thread = threading.Thread(target=asyncio.run, args=[client_manager.run()])
    client_manager_broadcast_thread.start()


def start_vue_server(host: str = "0.0.0.0", port: int = 8577) -> None:
    _logger.info(f"Starting Vue Server at {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_config=inject_logging_config())
