import logging
import os
from typing import Any

import redis

from database import Parameter


class DataStore:
    """

    """

    def __init__(self, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger("database")

        # Connect to Redis
        self._redis = redis.Redis(
            host=os.environ.get("REDIS_HOST", "localhost"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
        )
        self._logger.info("Redis connection established")

        # Initialize
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Initialize any parameters that are not yet in Redis
        """
        for param in Parameter:
            if not self.get(param):
                self._logger.info(f"Initializing '{param.name}' with default value: {param.default}")
                self.set(param, param.default)

    def get(self, param: Parameter) -> Any:
        try:
            return self._convert_post_redis(param, self._redis.get(param.name))
        except Exception as e:
            self._logger.error(f"Error: problem getting parameter '{param}' from redis.")
            self._logger.exception(e)
            raise e

    def set(self, param: Parameter, value: Any) -> None:
        try:
            return self._redis.set(param.name, self._convert_pre_redis(value))
        except Exception as e:
            self._logger.error(f"Error: problem setting parameter '{param}' in redis.")
            self._logger.exception(e)
            raise e

    @staticmethod
    def _convert_pre_redis(value: Any) -> Any:
        """
        Redis only accepts values that are Strings, Integers, or Floats. For all other datatypes (ex. booleans), the
        value must first be converted to a valid Redis type. This function is called during `set` operations.
        """
        # Handle: booleans
        if isinstance(value, bool):
            return str(value)
        # Handle: everything else
        else:
            return value

    @staticmethod
    def _convert_post_redis(param: Parameter, value: Any) -> Any:
        """
        Redis only contains values that are Strings, Integers, or Floats. For all other datatypes (ex. booleans), the
        value must be converted after it is read from Redis to the type we expect to receive. This function is called
        during `get` operations.
        """
        if value is None:
            return None  # likely means it hasn't yet been initialized
        else:
            # Handle: booleans
            if param.datatype == bool:
                return value.decode("utf-8") == "True"
            # Handle: everything else
            else:
                return param.datatype(value)
