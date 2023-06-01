from fastapi import APIRouter, Body

from fastapi_utils.cbv import cbv

from database import DataStore, Parameters

router = APIRouter()

sys_route = "/sys"  # prefix to add to all routes


# Example router class
@cbv(router)  # Class Based View router (cbv) uses python class structure
class SystemRoutes:
    def __init__(self):
        # TODO: need to do dependency injection to get DataStore class instance here
        self._data_store = DataStore()

    @router.post(f"{sys_route}/test", tags=["system"])
    async def test_route(self, value: dict = Body(...)):
        print(f"test: {value}")

    @router.get(f"{sys_route}/data", tags=["data"])
    async def get_all_data(self):
        values = {}
        i = 1
        for param in Parameters:
            values[param.name.lower()] = self._data_store.get(param)
        return values

    @router.post(f"{sys_route}/toggle-diff-lock", tags=["diff-lock"])
    async def toggle_diff_lock(self):
        self._data_store.set(Parameters.DIFFERENTIAL_LOCK, False if self._data_store.get(Parameters.DIFFERENTIAL_LOCK) else True)

    @router.post(f"{sys_route}/toggle-headlight-left", tags=["lights"])
    async def toggle_headlight_left(self):
        self._data_store.set(Parameters.HEADLIGHT_LEFT, False if self._data_store.get(Parameters.HEADLIGHT_LEFT) else True)

    @router.post(f"{sys_route}/toggle-headlight-right", tags=["lights"])
    async def toggle_headlight_right(self):
        self._data_store.set(Parameters.HEADLIGHT_RIGHT, False if self._data_store.get(Parameters.HEADLIGHT_RIGHT) else True)
