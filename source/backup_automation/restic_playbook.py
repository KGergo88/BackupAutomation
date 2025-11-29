from backup_automation.playbook import Playbook
from backup_automation.restic import Restic
from backup_automation.restic_playbook_steps import ResticPlaybookStep


class ResticPlaybook(Playbook[Restic]):
    """
    Class to represent a restic specific playbook.
    """
    def __init__(self, steps: tuple[ResticPlaybookStep, ...]):
        self.__steps = steps

    def execute(self, backup_backend: Restic) -> None:
        """
        Execute the playbook with the given backup backend.
        """
        for step in self.__steps:
            step.execute(backup_backend)
