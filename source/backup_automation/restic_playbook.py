from restic import Restic
from restic_playbook_steps import ResticPlaybookStep


class ResticPlaybook:
    def __init__(self, steps: tuple[ResticPlaybookStep, ...]):
        self.__steps = steps

    def execute(self, restic: Restic):
        for step in self.__steps:
            step.execute(restic)
