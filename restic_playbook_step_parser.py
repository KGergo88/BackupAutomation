import pathlib
from typing import Callable, Collection

from restic_playbook_exception import ResticPlaybookException
from restic_playbook_steps import ResticPlaybookStep, ResticPlaybookBackupStep
from restic_repository import ResticRepository


class ResticPlaybookStepParser:
    STEPS_COMMAND_BACKUP = "backup"

    def __init__(self, repository_lookup: Callable[[str], ResticRepository]):
        self.__repository_lookup = repository_lookup

    def parse(self, step_json: dict):
        step_command = step_json[ResticPlaybookStep.STEPS_COMMAND_KEY]
        match step_command:
            case ResticPlaybookStepParser.STEPS_COMMAND_BACKUP:
                return self.__parse_backup_step(step_json)
            case _:
                raise ResticPlaybookException(f"Unexpected command in step: {step_json}")

    def __parse_backup_step(self, step_json: dict) -> ResticPlaybookBackupStep:
        repository_name = step_json[ResticPlaybookBackupStep.REPOSITORY_KEY]
        repository = self.__repository_lookup(repository_name)

        source_path = pathlib.Path(step_json[ResticPlaybookBackupStep.SOURCE_PATH_KEY])
        if not source_path.is_dir():
            raise ResticPlaybookException(f"Source path is not a valid directory: {self.__source_path}")

        tags = step_json.get(ResticPlaybookBackupStep.TAGS_KEY, [])
        if not isinstance(tags, list):
            raise ResticPlaybookException(f"Tags is not a valid JSON array: {tags}")

        return ResticPlaybookBackupStep(repository, source_path, tuple(tags))