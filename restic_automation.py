import argparse
import logging
import pathlib

from restic import Restic
from restic_playbook_parser import ResticPlaybookParser


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting restic automation")

    args = parse_arguments()
    logger.info(f"Received arguments: {args}")

    restic = Restic(args.dry_mode, args.verbose)

    logger.info(f"Parsing playbook: {args.playbook}")
    playbook = ResticPlaybookParser(args.no_interaction).parse(args.playbook)

    logger.info(f"Executing playbook: {playbook}")
    playbook.execute(restic)


def parse_arguments():
    parser = argparse.ArgumentParser(prog="Restic Automation")
    parser.add_argument("--playbook",
                        type=pathlib.Path,
                        required=True,
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

    parsed_arguments = parser.parse_args()
    return parsed_arguments


if "__main__" == __name__:
    main()
