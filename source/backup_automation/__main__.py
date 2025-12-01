import argparse
import logging
import pathlib

from backup_automation import __version__
from backup_automation.backend import BackendSettings
from backup_automation.playbook_parser import PlaybookParserSettings
from backup_automation.playbook_parser_factory import PlaybookParserFactory


def main() -> None:
    """
    The main function of the package.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s][%(name)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    args = parse_arguments()

    logger.info("Starting backup automation")
    logger.info("Received arguments: %s", args)

    playbook_parser_settings = PlaybookParserSettings(no_interaction = args.no_interaction)
    backend_settings = BackendSettings(dry_mode = args.dry_mode, verbose = args.verbose)

    playbook_parser = PlaybookParserFactory.create_from_file(args.playbook, playbook_parser_settings, backend_settings)

    logger.info("Parsing playbook: %s", args.playbook)
    playbook = playbook_parser.parse(args.playbook)

    logger.info("Executing playbook: %s", playbook)
    playbook.execute()
    logger.info("Finished executing playbook!")


def parse_arguments() -> argparse.Namespace:
    """
    Function to parse the command line arguments.
    """
    parser = argparse.ArgumentParser(prog="Backup Automation")
    parser.add_argument("playbook",
                        type=pathlib.Path,
                        help="Filepath of a playbook")
    parser.add_argument("--dry-mode",
                        action="store_true",
                        help="Commands will be logged but not executed. No restic executable is needed.")
    parser.add_argument("--no-interaction",
                        action="store_true",
                        help="No user interactions will be made. The program will fail if user input would be needed.")
    parser.add_argument("--verbose",
                        action="store_true",
                        help="Verbose mode. More information will be printed.")
    parser.add_argument("--version",
                        action="version",
                        version=f"%(prog)s v{__version__}",
                        help="Show program's version and exit.")

    parsed_arguments = parser.parse_args()
    return parsed_arguments


if "__main__" == __name__:
    main()
