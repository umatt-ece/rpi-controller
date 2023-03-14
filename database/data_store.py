import redis
from typing import Union, Any
from database import LiveData, StoredData


class DataStore:

    def __init__(self):
        self._live_redis = redis.Redis(host="localhost", port=6379, db=0)
        self._stored_redis = redis.Redis(host="localhost", port=6379, db=1)
        # self._logger  # TODO: implement logging

        # Initialize
        self.initialize_database()

    def initialize_database(self):
        # Initialize the Live Data Store if it has not been yet.
        if not self.get(LiveData.INITIALIZED):
            print('Initializing Live Redis Database')
            for entry in LiveData:
                self.set(entry, entry.default)
        # Initialize the Stored Data Store if it has not been yet.
        if not self.get(StoredData.INITIALIZED):
            print('Initializing Stored Redis Database')
            for entry in StoredData:
                self.set(entry, entry.default)

    def get(self, param: Union[LiveData, StoredData]):
        if isinstance(param, LiveData):
            return self._convert_post_redis(param, self._live_redis.get(param.name))
        elif isinstance(param, StoredData):
            return self._convert_post_redis(param, self._stored_redis.get(param.name))
        else:
            raise KeyError(f"'{param}' is not a valid parameter")

    def set(self, param: Union[LiveData, StoredData], value: Any):
        if isinstance(param, LiveData):
            return self._live_redis.set(param.name, self._convert_pre_redis(value))
        elif isinstance(param, StoredData):
            return self._stored_redis.set(param.name, self._convert_pre_redis(value))
        else:
            raise KeyError(f"'{param}' is not a valid parameter")

    def get_many(self, params: list) -> dict:
        pass

    def set_many(self, params: dict):
        pass

    @staticmethod
    def _convert_pre_redis(value):
        if isinstance(value, bool):
            return str(value)
        else:
            return value

    @staticmethod
    def _convert_post_redis(param, value):
        if isinstance(param.datatype, bool):
            return value.decode('utf-8') == 'True'
        else:
            return param.datatype(value)


# FOR TESTING...
if __name__ == "__main__":
    print("testing data store...")
    data_store = DataStore()
    print(f'live parameters initialized: {data_store.get(LiveData.INITIALIZED)} {type(data_store.get(LiveData.INITIALIZED))}')
    print(f'stored parameters initialized: {data_store.get(LiveData.INITIALIZED)} {type(data_store.get(StoredData.INITIALIZED))}')

    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')
    data_store.set(LiveData.SPEED, 123.0)
    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')
    data_store.set(LiveData.SPEED, 321)
    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')

    print(f'speed: {data_store.get(LiveData.GEAR)} {type(data_store.get(LiveData.GEAR))}')
    data_store.set(LiveData.GEAR, 3)
    print(f'speed: {data_store.get(LiveData.GEAR)} {type(data_store.get(LiveData.GEAR))}')



