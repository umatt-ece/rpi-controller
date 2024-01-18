"""
Package: Logic
Purpose: This module contains all the 'logical' code for the controller - the state machines that control the tractor
         functionality. This code is specifically tied to a particular tractor design.
"""
from .base_state_machine import BaseStateMachine, DEFAULT_INTERVAL
from .evt_state_machine import EVTStateMachine
from .demo_state_machine import DemoStateMachine
