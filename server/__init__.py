"""
Package: server
Purpose: This module contains the code for hosting a REST API server and VueJS app as the controller's interface. The
         vue-app code is in a different repository (display-frontend), this code is just to host and service it.
"""
from .client_manager import ClientManager
from .system_routes import router as system_router

from .vue_server import start_vue_server
