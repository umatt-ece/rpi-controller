from fastapi import APIRouter, Body

from fastapi_utils.cbv import cbv

from database import DataStore, LiveData as lD

router = APIRouter()

sys_route = "/sys"  # prefix to add to all routes


# Example router class
@cbv(router)  # Class Based View router (cbv) uses python class structure
class SystemRoutes:
    def __init__(self):
        # TODO: need to do dependency injection to get DataStore class instance here
        pass

    @router.post(f"{sys_route}/test", tags=["system"])
    async def get_all_data(self):
        data_store = DataStore()
        data_store.set(lD.TEST_PARAM, False if data_store.get(lD.TEST_PARAM) else True)

    @router.get(f"{sys_route}/get", tags=["system"])
    async def get_all_data(self):
        return [{"boolean": True}, {"string": "Success"}, {"list": [1, 2, 3]}]

    @router.post(f"{sys_route}/post", tags=["system"])
    async def do_something(self, value: dict = Body(...)):
        print(f"value: {value}")
