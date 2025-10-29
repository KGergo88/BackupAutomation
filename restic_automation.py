import argparse
import logging
import pathlib

from restic import Restic
from restic_playbook_parser import ResticPlaybookParser


def main(arguments: argparse.Namespace):
    restic = Restic(arguments.dry_mode)
    playbook = ResticPlaybookParser(arguments.no_interaction).parse(arguments.playbook)
    playbook.execute(restic)


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)

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

    parsed_arguments = parser.parse_args()

    main(parsed_arguments)
