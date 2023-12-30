import os
from typing import Any, Union

import redis

from src.database import Parameters


class DataStore:

    def __init__(self):
        self._redis = redis.Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
        )
        # self._logger  # TODO: implement logging

        # Initialize
        self.initialize_database()

    def initialize_database(self):
        # Initialize the Data Store if it has not been yet
        if not self.get(Parameters.INITIALIZED):
            print('Initializing Redis...')
            for entry in Parameters:
                self.set(entry, entry.default)

    def get(self, param: Parameters):
        try:
            return self._convert_post_redis(param, self._redis.get(param.name))
        except Exception as e:
            raise Exception(f"Error: problem getting parameter '{param}' from redis.")

    def set(self, param: Parameters, value: Any):
        try:
            return self._redis.set(param.name, self._convert_pre_redis(value))
        except Exception as e:
            raise Exception(f"Error: problem setting parameter '{param}' in redis.")

    @staticmethod
    def _convert_pre_redis(value):
        if isinstance(value, bool):
            return str(value)
        else:
            return value

    @staticmethod
    def _convert_post_redis(param: Parameters, value):
        if param.datatype == bool:
            if param == Parameters.INITIALIZED and value is None:
                return False
            return value.decode("utf-8") == "True"
        else:
            return param.datatype(value)
