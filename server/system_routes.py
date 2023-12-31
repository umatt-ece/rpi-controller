import logging
from fastapi import APIRouter, Body
from fastapi_utils.cbv import cbv

from common import get_data_store
from database import DataStore, Parameter

router = APIRouter()


@cbv(router)
class SystemRoutes:
    def __init__(self):
        self._logger = logging.getLogger("server")
        self._data_store = get_data_store()

    @router.post("/api/test", tags=["Testing"])
    async def test_route(self, value: dict = Body(...)):
        self._logger.info(f"Testing...")
