from fastapi import APIRouter, Body

router = APIRouter()
data_routes = "/data/"


@router.get(data_routes + "all")
async def get_all_data():
    return [{"data1": 1234567890}, {"data2": "Success"}, {"data3": ["One", "Two", "Three"]}]


@router.post(data_routes + "do")
async def do_something(value: dict = Body(...)):
    print(f"value: {value}")
