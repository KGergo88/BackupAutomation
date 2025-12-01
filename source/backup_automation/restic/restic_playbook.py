from backup_automation.playbook import Playbook
from backup_automation.restic.restic_playbook_steps import ResticPlaybookStep


class ResticPlaybook(Playbook):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment.
    """
    Class to represent a restic specific playbook.
    """
    def __init__(self, steps: tuple[ResticPlaybookStep, ...]):
        self.__steps = steps

    def execute(self) -> None:
        """
        Execute the playbook with the given backend.
        """
        for step in self.__steps:
            step.execute()
