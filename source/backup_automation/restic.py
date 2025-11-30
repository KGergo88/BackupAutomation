import logging
import pathlib
import subprocess

from backup_automation.backup_backend import BackupBackend, BackupBackendSettings
from backup_automation.restic_exception import ResticException
from backup_automation.restic_repository import ResticRepository
from backup_automation.temporary_environment_variables import TemporaryEnvironmentVariables


class Restic(BackupBackend):
    """
    Class that represents the restic backup software.
    """
    RESTIC_URL = "https://restic.net"
    RESTIC_EXECUTABLE = "restic"
    RESTIC_PASSWORD_ENVIRONMENT_VARIABLE = "RESTIC_PASSWORD"
    RESTIC_FROM_PASSWORD_ENVIRONMENT_VARIABLE = "RESTIC_FROM_PASSWORD"

    def __init__(self,
                 settings: BackupBackendSettings,
                 logger: logging.Logger = logging.getLogger(__name__)):
        self.__logger = logger

        self.__dry_mode = settings.dry_mode
        if self.__dry_mode:
            self.__logger.info("Dry mode was requested, commands will only be logged and not executed!")

        self.__verbose = settings.verbose

        self.__logger.info("Looking for %s", Restic.RESTIC_EXECUTABLE)
        command = [
            Restic.RESTIC_EXECUTABLE,
            "version"
        ]
        self.__execute_command(command,
                               f"Could not find {Restic.RESTIC_EXECUTABLE}! Please install it from {Restic.RESTIC_URL}")

    def backup(self, repository: ResticRepository, source_path: pathlib.Path, tags: tuple[str, ...] = ()) -> None:
        """
        Backup the source path content to the repository and apply the tags to the snapshots.
        Link: https://restic.readthedocs.io/en/stable/040_backup.html
        """
        log_tags_part = f" with tags [{", ".join(tags)}]" if tags else ""
        self.__logger.info(f"Backing up \"{source_path}\" to repository \"{repository.name}\"{log_tags_part}")

        command_tags_part = []
        for tag in tags:
            command_tags_part.append("--tag")
            command_tags_part.append(f"{tag}")

        command_verbose_part = []
        if self.__verbose:
            command_verbose_part.append("--verbose")

        command = [
            Restic.RESTIC_EXECUTABLE,
            "backup",
            "--repo", str(repository.uri),
            *command_verbose_part,
            *command_tags_part,
            str(source_path)
        ]

        environment_variables = {
            Restic.RESTIC_PASSWORD_ENVIRONMENT_VARIABLE: repository.password
        }
        with TemporaryEnvironmentVariables(environment_variables):
            self.__execute_command(command)

    def copy(self, source_repository: ResticRepository, target_repository: ResticRepository) -> None:
        """
        Copy snapshots from the source repository to the target repository.
        Link: https://restic.readthedocs.io/en/stable/045_working_with_repos.html#copying-snapshots-between-repositories
        """
        command_verbose_part = []
        if self.__verbose:
            command_verbose_part.append("--verbose")

        command = [
            Restic.RESTIC_EXECUTABLE,
            "copy",
            "--from-repo", str(source_repository.uri),
            "--repo", str(target_repository.uri),
            *command_verbose_part
        ]

        environment_variables = {
            Restic.RESTIC_FROM_PASSWORD_ENVIRONMENT_VARIABLE: source_repository.password,
            Restic.RESTIC_PASSWORD_ENVIRONMENT_VARIABLE: target_repository.password
        }
        with TemporaryEnvironmentVariables(environment_variables):
            self.__execute_command(command)

    def __execute_command(self, command: list[str], custom_error_message: str | None = None) -> None:
        self.__logger.info(f"Executing command: \"{" ".join(command)}\"")
        if self.__dry_mode:
            return

        try:
            subprocess.run(command, check=True)
        except Exception as e:
            if custom_error_message:
                raise ResticException(custom_error_message, e) from e

            raise ResticException(f"Failed to execute command: \"{command}\"", e) from e
