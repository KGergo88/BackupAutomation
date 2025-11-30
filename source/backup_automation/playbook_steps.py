from abc import ABC, abstractmethod


class PlaybookStep(ABC):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Abstract class to represent a playbook step.
    Steps represent a specific action in a playbook that shall be done with the backend.
    """
    @abstractmethod
    def execute(self) -> None:
        """
        Execute the step with the given backend.
        """
