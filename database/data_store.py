import os
from typing import Any, Union

import redis

from database import LiveData, StoredData


class DataStore:

    def __init__(self):
        self._live_redis = redis.Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            db=0,
        )
        self._stored_redis = redis.Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            db=1
        )
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
        live_params = []
        stored_params = []
        results = {}

        for entry in params:
            if isinstance(entry, LiveData):
                live_params.append(entry)
            elif isinstance(entry, StoredData):
                stored_params.append(entry)
            else:
                raise KeyError(f"'{entry}' is not a valid parameter")

        if live_params:
            live_values = self._live_redis.mget([data.name for data in live_params])
            for i in range(len(live_params)):
                results[live_params[i].name] = self._convert_post_redis(live_params[i], live_values[i])
        if stored_params:
            stored_values = self._stored_redis.mget([data.name for data in stored_params])
            for i in range(len(stored_params)):
                results[stored_params[i].name] = self._convert_post_redis(stored_params[i], stored_values[i])

        return results

    def set_many(self, params: dict):
        live_params = {}
        stored_params = {}

        for entry, value in params.items():
            if isinstance(entry, LiveData):
                live_params[entry] = self._convert_pre_redis(value)
            elif isinstance(entry, StoredData):
                stored_params[entry] = self._convert_pre_redis(value)
            else:
                raise KeyError(f"'{entry}' is not a valid parameter")

        if live_params:
            self._live_redis.mset(live_params)
        if live_params:
            self._live_redis.mset(live_params)

    @staticmethod
    def _convert_pre_redis(value):
        if isinstance(value, bool):
            return str(value)
        elif isinstance(value, list):
            return str(value)
        else:
            return value

    @staticmethod
    def _convert_post_redis(param: Union[LiveData, StoredData], value):
        if param.datatype == bool:
            return value.decode("utf-8") == "True"
        elif param.datatype == list:
            # covert list from string to list of strings
            value_list = value.decode("utf-8").strip("[]").split(",").strip()
            print(value_list)
            # attempt to cast values into their datatype (supports: bool, int, str)
            for i in range(len(value_list)):
                if value_list[i] == "False" or value_list == "True":
                    value_list[i] = value_list[i] == "True"
                elif value_list[i].isdigit():
                    value_list[i] = int(value_list[i])
                else:
                    pass  # already string
            print(value_list)
            return value_list
        else:
            return param.datatype(value)


# FOR TESTING...
if __name__ == "__main__":
    print("testing data store...")
    data_store = DataStore()
    print(
        f'live parameters initialized: {data_store.get(LiveData.INITIALIZED)} {type(data_store.get(LiveData.INITIALIZED))}')
    print(
        f'stored parameters initialized: {data_store.get(LiveData.INITIALIZED)} {type(data_store.get(StoredData.INITIALIZED))}')

    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')
    data_store.set(LiveData.SPEED, 123.0)
    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')
    data_store.set(LiveData.SPEED, 321)
    print(f'speed: {data_store.get(LiveData.SPEED)} {type(data_store.get(LiveData.SPEED))}')

    print(f'speed: {data_store.get(LiveData.GEAR)} {type(data_store.get(LiveData.GEAR))}')
    data_store.set(LiveData.GEAR, 3)
    print(f'speed: {data_store.get(LiveData.GEAR)} {type(data_store.get(LiveData.GEAR))}')
