import pathlib
from typing import Callable

from backup_automation.restic.restic_backend import ResticBackend
from backup_automation.restic.restic_playbook_exception import ResticPlaybookException
from backup_automation.restic.restic_playbook_format import ResticPlaybookFormat
from backup_automation.restic.restic_playbook_steps import (ResticPlaybookStep,
                                                            ResticPlaybookBackupStep,
                                                            ResticPlaybookCopyStep)
from backup_automation.restic.restic_repository import ResticRepository
from backup_automation.typehints import JsonDict


class ResticPlaybookStepParser:
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent a restic specific playbook step parser.
    """
    def __init__(self, backend: ResticBackend, repository_lookup: Callable[[str], ResticRepository]):
        self.__backend = backend
        self.__repository_lookup = repository_lookup
        self.__format = ResticPlaybookFormat()

    def parse(self, step_json: JsonDict) -> ResticPlaybookStep:
        """
        Parses a playbook step from received JSON object into a ResticPlaybookStep object.
        """
        step_command = step_json[self.__format.STEPS_COMMAND_KEY]
        match step_command:
            case self.__format.STEPS_COMMAND_VALUE_BACKUP:
                return self.__parse_backup_step(step_json)
            case self.__format.STEPS_COMMAND_VALUE_COPY:
                return self.__parse_copy_step(step_json)
            case _:
                raise ResticPlaybookException(f"Unexpected command in step: {step_json}")

    def __parse_backup_step(self, step_json: JsonDict) -> ResticPlaybookBackupStep:
        repository_id = step_json.get(self.__format.STEPS_BACKUP_REPOSITORY_KEY, None)
        if repository_id is None:
            raise ResticPlaybookException(f"Missing required key for backup step: {self.__format.STEPS_BACKUP_REPOSITORY_KEY}")

        repository = self.__repository_lookup(repository_id)

        raw_source_path = step_json.get(self.__format.STEPS_BACKUP_SOURCE_PATH_KEY, None)
        if raw_source_path is None:
            raise ResticPlaybookException(f"Missing required key for backup step: {self.__format.STEPS_BACKUP_SOURCE_PATH_KEY}")

        source_path = pathlib.Path(raw_source_path)

        tags = step_json.get(self.__format.STEPS_BACKUP_TAGS_KEY, [])
        if not isinstance(tags, list):
            raise ResticPlaybookException(f"Tags is not a valid JSON array: {tags}")

        raw_working_dir = step_json.get(self.__format.STEPS_BACKUP_WORKING_DIR_KEY, None)
        working_dir = pathlib.Path(raw_working_dir) if raw_working_dir else None

        if working_dir:
            if source_path.is_absolute():
                raise ResticPlaybookException(f"If working_dir is defined, source_path must be a relative path!"
                                              f" working_dir: {working_dir} source_path: {source_path}")

            path_to_backup = working_dir / source_path
            if not path_to_backup.is_dir():
                raise ResticPlaybookException(f"The path to backup (combination of working_dir and source_path)"
                                              f" is not a valid directory: {path_to_backup}")
        else:
            if not source_path.is_absolute():
                raise ResticPlaybookException(f"If working_dir is not defined, source_path must be an absolute path! "
                                              f"source_path: {source_path}")

            if not source_path.is_dir():
                raise ResticPlaybookException(f"The path to backup (source_path)"
                                              f" is not a valid directory: {source_path}")

        return ResticPlaybookBackupStep(self.__backend, repository, source_path, tuple(tags), working_dir)

    def __parse_copy_step(self, step_json: JsonDict) -> ResticPlaybookCopyStep:
        source_repository_id = step_json.get(self.__format.STEPS_COPY_SOURCE_REPOSITORY_KEY, None)
        if source_repository_id is None:
            raise ResticPlaybookException(f"Missing required key for copy step: {self.__format.STEPS_COPY_SOURCE_REPOSITORY_KEY}")

        source_repository = self.__repository_lookup(source_repository_id)

        target_repository_id = step_json.get(self.__format.STEPS_COPY_TARGET_REPOSITORY_KEY, None)
        if target_repository_id is None:
            raise ResticPlaybookException(f"Missing required key for copy step: {self.__format.STEPS_COPY_TARGET_REPOSITORY_KEY}")

        target_repository = self.__repository_lookup(target_repository_id)

        if source_repository == target_repository:
            raise ResticPlaybookException("The source and target repositories cannot be the same!")

        return ResticPlaybookCopyStep(self.__backend, source_repository, target_repository)
