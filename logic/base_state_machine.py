import logging
import time

DEFAULT_INTERVAL = 1  # seconds


class BaseStateMachine:
    """
    This class is a state machine 'interface'. It defines all the basic components of a state machine but does not
    actually implement one itself (this is help reduce the amount of duplicated code fragments and maintain consistency
    across all state machines). Rather, other state machines should inherit from this class and should implement and
    build upon the existing functionality
    """
    _last_run_time = time.perf_counter()
    _state = None

    def __init__(self, name: str, initial_state: str, interval: int = DEFAULT_INTERVAL, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger("logic")
        self._name = name
        self._interval = interval

        self._state = self.validate_state(initial_state)

    @staticmethod
    def run_forever():
        """
        This is the default 'stop_thread' condition for BaseStateMachine instances if no external  function is provided.
        It will always return True and thus the thread will run indefinitely unless forcefully stopped by the
        operating system. It is best to override this function and provide an external stop condition.
        """
        return True

    def update(self) -> None:
        raise NotImplementedError(f"The `update` function must be implemented by subclasses.")

    def step(self) -> None:
        raise NotImplementedError(f"The `step` function must be implemented by subclasses.")

    def transition(self) -> None:
        # Check all transition conditions for the current state
        for transition, details in self.states()[self._state]["transitions"].items():
            for condition in details["conditions"]:
                if condition():

                    # Call "on_exit" function of previous state (optional)
                    if on_exit_functions := self.states[self._state]['on_exit']:
                        for function in on_exit_functions:
                            function()

                    # Transition to next state
                    self._logger.info(f"{self.name}: Transitioning from '{self._state}' to '{details['next_state']}' " +
                                      f"on condition '{condition.__name__}'")
                    self._state = details["next_state"]

                    # Call "on_enter" function of next state (optional)
                    if on_enter_functions := self.states[self._state]['on_enter']:
                        for function in on_enter_functions:
                            function()

    def run(self, stop_thread: callable = run_forever) -> None:
        try:
            self._logger.info(f"Thread '{self.name}' started successfully")

            # The `stop_thread` function allows outside processes to stop this thread gracefully
            while not stop_thread():
                # Record time at start of current step
                self._last_run_time = time.perf_counter()
                self._logger.debug(f"Thread '{self.name}' running at {time.perf_counter()}")

                self.update()      # Update local variable
                self.step()        # Run current state functions
                self.transition()  # Transition to the next state

                # Release processor until next timer interval
                time.sleep((self._last_run_time + self._interval) - time.perf_counter())

            # Exit the thread gracefully
            self._logger.info(f"Stopping thread '{self.name}' due to external signal")

        except Exception as e:
            self._logger.exception(e)
            raise e

    def validate_state(self, state: str) -> str:
        if state not in self.states():
            raise Exception(
                f"'{state}' is not a valid state for '{self.name}' (states: {[state for state in self.states.keys()]})")
        return state

    @property
    def states(self):
        """
        Dictionary representation of the state machine. The `states` dictionary must follow a particular structure, as
        shown below. Every state MUST include at least 1 transition; however, the `on_enter` and `on_exit` properties
        are optional.

        example = {
            "state_0": {
                "on_enter": [callable],             (optional)
                "on_exit": [callable],              (optional)
                "transitions": {                    (required)
                    "transition_0": {
                        "next_state": "state_1",    (required)
                        "conditions": [callable],   (required)
                    }
                }
            }
        }
        """
        raise NotImplementedError("The `states` property must be implemented by subclasses.")

    @property
    def name(self) -> str:
        return self._name


INTERVAL = 1
