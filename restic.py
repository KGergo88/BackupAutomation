import logging
import pathlib
import subprocess

from restic_exception import ResticException
from restic_repository import ResticRepository
from temporary_environment_variable_setter import TemporaryEnvironmentVariableSetter


class Restic:
    RESTIC_URL = "https://restic.net"
    RESTIC_EXECUTABLE = "restic"
    RESTIC_PASSWORD_ENVIRONMENT_VARIABLE = "RESTIC_PASSWORD"
    RESTIC_FROM_PASSWORD_ENVIRONMENT_VARIABLE = "RESTIC_FROM_PASSWORD"

    def __init__(self, dry_mode: bool = False, verbose: bool = False):
        self.__dry_mode = dry_mode
        if self.__dry_mode:
            logging.info(f"Dry mode was requested, commands will only be logged and not executed!")

        self.__verbose = verbose

        logging.info(f"Looking for {Restic.RESTIC_EXECUTABLE}")
        command = [
            Restic.RESTIC_EXECUTABLE,
            "version"
        ]
        self.__execute_command(command, f"Could not find {Restic.RESTIC_EXECUTABLE}! Please install it from {Restic.RESTIC_URL}")

    def backup(self, repository: ResticRepository, source_path: pathlib.Path, tags: tuple[str, ...] = ()):
        log_tags_part = f" with tags [{", ".join(tags)}]" if tags else ""
        logging.info(f"Backing up \"{source_path}\" to repository \"{repository.name}\"{log_tags_part}")

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
            "--repo", str(repository.path),
            *command_verbose_part,
            *command_tags_part,
            str(source_path)
        ]

        environment_variables = {
            Restic.RESTIC_PASSWORD_ENVIRONMENT_VARIABLE: repository.password
        }
        with TemporaryEnvironmentVariableSetter(environment_variables):
            self.__execute_command(command)

    def copy(self, source_repository: ResticRepository, target_repository: ResticRepository):
        command_verbose_part = []
        if self.__verbose:
            command_verbose_part.append("--verbose")

        command = [
            Restic.RESTIC_EXECUTABLE,
            "copy",
            "--from-repo", str(source_repository.path),
            "--repo", str(target_repository.path),
            *command_verbose_part
        ]

        environment_variables = {
            Restic.RESTIC_FROM_PASSWORD_ENVIRONMENT_VARIABLE: source_repository.password,
            Restic.RESTIC_PASSWORD_ENVIRONMENT_VARIABLE: target_repository.password
        }
        with TemporaryEnvironmentVariableSetter(environment_variables):
            self.__execute_command(command)

    def __execute_command(self, command: list[str], custom_error_message: str | None = None):
        logging.info(f"Executing command: \"{" ".join(command)}\"")
        if self.__dry_mode:
            return

        try:
            subprocess.run(command, check=True)
        except Exception as e:
            if custom_error_message:
                raise ResticException(custom_error_message, e) from e
            else:
                raise ResticException(f"Failed to execute command: \"{command}\"", e) from e
