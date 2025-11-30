import pathlib
from typing import Callable

from backup_automation.restic import Restic
from backup_automation.restic_playbook_exception import ResticPlaybookException
from backup_automation.restic_playbook_steps import ResticPlaybookStep, ResticPlaybookBackupStep, ResticPlaybookCopyStep
from backup_automation.restic_repository import ResticRepository
from backup_automation.typehints import JsonDict


class ResticPlaybookStepParser:
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent a restic specific playbook step parser.
    """
    STEPS_COMMAND_BACKUP = "backup"
    STEPS_COMMAND_COPY = "copy"

    def __init__(self, backend: Restic, repository_lookup: Callable[[str], ResticRepository]):
        self.__backend = backend
        self.__repository_lookup = repository_lookup

    def parse(self, step_json: JsonDict) -> ResticPlaybookStep:
        """
        Parses a playbook step from received JSON object into a ResticPlaybookStep object.
        """
        step_command = step_json[ResticPlaybookStep.STEPS_COMMAND_KEY]
        match step_command:
            case ResticPlaybookStepParser.STEPS_COMMAND_BACKUP:
                return self.__parse_backup_step(step_json)
            case ResticPlaybookStepParser.STEPS_COMMAND_COPY:
                return self.__parse_copy_step(step_json)
            case _:
                raise ResticPlaybookException(f"Unexpected command in step: {step_json}")

    def __parse_backup_step(self, step_json: JsonDict) -> ResticPlaybookBackupStep:
        repository_name = step_json[ResticPlaybookBackupStep.REPOSITORY_KEY]
        repository = self.__repository_lookup(repository_name)

        source_path = pathlib.Path(step_json[ResticPlaybookBackupStep.SOURCE_PATH_KEY])
        if not source_path.is_dir():
            raise ResticPlaybookException(f"Source path is not a valid directory: {source_path}")

        tags = step_json.get(ResticPlaybookBackupStep.TAGS_KEY, [])
        if not isinstance(tags, list):
            raise ResticPlaybookException(f"Tags is not a valid JSON array: {tags}")

        return ResticPlaybookBackupStep(self.__backend, repository, source_path, tuple(tags))

    def __parse_copy_step(self, step_json: JsonDict) -> ResticPlaybookCopyStep:
        source_repository_name = step_json[ResticPlaybookCopyStep.SOURCE_REPOSITORY_KEY]
        source_repository = self.__repository_lookup(source_repository_name)

        target_repository_name = step_json[ResticPlaybookCopyStep.TARGET_REPOSITORY_KEY]
        target_repository = self.__repository_lookup(target_repository_name)

        if source_repository == target_repository:
            raise ResticPlaybookException("The source and target repositories cannot be the same!")

        return ResticPlaybookCopyStep(self.__backend, source_repository, target_repository)
