import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from routers import WebsocketRoutes, data_router, system_router
from services import ClientManager


def create_app() -> FastAPI:
    new_app = FastAPI()
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.include_router(data_router)
    new_app.include_router(system_router)
    new_app.add_websocket_route('/ws', WebsocketRoutes)
    new_app.mount("/", StaticFiles(directory="vue-app", html=True), name="VueJS App")
    return new_app


app = create_app()


@app.get("/")
async def vuejs_app():
    return FileResponse('vue-app/index.html', media_type='text/html')


@app.on_event('startup')
async def app_startup():
    client_manager = ClientManager()
    asyncio.create_task(client_manager.run())


# def counting():
#     value = 0
#     while True:
#         time.sleep(1)
#         print(value)
#         value += 1


def main():
    # initialization
    print('Starting UMATT Server Application')
    uvicorn.run(app, host="localhost", port=8577)


if __name__ == "__main__":
    main()
