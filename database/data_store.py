import redis
from typing import Union, Any
from database import LiveData, StoredData


class DataStore:

    def __init__(self):
        self._live_redis = redis.Redis(host="localhost", port=6379, db=0)
        self._stored_redis = redis.Redis(host="localhost", port=6379, db=1)
        # self._logger  # TODO: implement logging

    def initialize_database(self):
        for entry in LiveData:
            self._live_redis.set(entry.name, entry.datatype())
        for entry in StoredData:
            pass

    def set(self, key: Union[LiveData, StoredData], value: Any):
        if isinstance(key, LiveData):
            return self._live_redis.set(key.name, value)
        elif isinstance(key, StoredData):
            return self._stored_redis.set(key.name, value)
        else:
            raise KeyError(f"'{key}' is not a valid parameter")

    def get(self, key: Union[LiveData, StoredData]):
        if isinstance(key, LiveData):
            return self._live_redis.get(key.name)
        elif isinstance(key, StoredData):
            return self._stored_redis.get(key.name)
        else:
            raise KeyError(f"'{key}' is not a valid parameter")

    def get_many(self, keys: list):
        pass

    def set_many(self, key_values: dict):
        pass
