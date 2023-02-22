from fastapi import APIRouter, Body

from fastapi_utils.cbv import cbv

router = APIRouter()

data_route = "/data"  # prefix to add to all routes


# Example router class
@cbv(router)  # Class Based View router (cbv) uses python class structure
class DataRoutes:
    def __init__(self):
        # TODO: need to do dependency injection to get DataStore class instance here
        pass

    @router.get(f"{data_route}/get", tags=["data"])
    async def get_all_data(self):
        return [{"boolean": True}, {"string": "Success"}, {"list": [1, 2, 3]}]

    @router.post(f"{data_route}/post", tags=["data"])
    async def do_something(self, value: dict = Body(...)):
        print(f"value: {value}")
