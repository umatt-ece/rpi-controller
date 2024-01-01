"""
This file is intended to reduce the number of instances of class dependency created throughout the execution of this
project. By creating a central location for class dependencies, files from all areas of the program can access the
same instances of a given class.
"""
import logging

from database import DataStore
from server import ClientManager
from hardware import RaspberryPi

# Global 'singleton' objects (there should only ever be a single instantiation of this class throughout the project)
data_store_singleton = None
client_manager_singleton = None
raspberry_pi_singleton = None


def get_data_store(logger: logging.Logger = None) -> DataStore:
    # Need to access globally stored `data_store_singleton`
    global data_store_singleton

    # If it hasn't been instantiated yet, do so
    if data_store_singleton is None:
        data_store_singleton = DataStore(logger)

    # Return single instance of class
    return data_store_singleton


def get_client_manager(logger: logging.Logger = None) -> ClientManager:
    # Need to access globally stored `client_manager_singleton`
    global client_manager_singleton

    # If it hasn't been instantiated yet, do so
    if client_manager_singleton is None:
        client_manager_singleton = ClientManager(logger)

    # Return single instance of class
    return client_manager_singleton


def get_raspberry_pi(model: str, logger: logging.Logger = None) -> RaspberryPi:
    # Need to access globally stored `raspberry_pi_singleton`
    global raspberry_pi_singleton

    # If it hasn't been instantiated yet, do so
    if raspberry_pi_singleton is None:
        raspberry_pi_singleton = RaspberryPi(model, logger)

    # Return single instance of class
    return raspberry_pi_singleton
