"""
This file is intended to reduce the number of instances of class dependency created throughout the execution of this
project. By creating a central location for class dependencies, files from all areas of the program can access the
same instances of a given class.
"""
import logging

from database import DataStore

# Global 'singleton' objects (there should only ever be a single instantiation of this class throughout the project)
data_store_singleton = None


def get_data_store(logger: logging.Logger = None) -> DataStore:
    # Need to access globally stored `data_store_singleton`
    global data_store_singleton

    # If it hasn't been instantiated yet, do so
    if data_store_singleton is None:
        data_store_singleton = DataStore(logger)

    # Return single instance of class
    return data_store_singleton
