from abc import ABC, abstractmethod

from backup_automation.playbook_steps import PlaybookStep


class Playbook(ABC):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment, but we need it to enforce interface for subclasses.
    """
    Abstract class to represent a playbook.
    Playbooks orchestrate the backup operations.
    They contain steps that execute an action on the Backend.
    """
    @abstractmethod
    def __init__(self, steps: tuple[PlaybookStep]) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the playbook with the given backend.
        """
