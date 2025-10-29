import logging

from restic import Restic
from restic_repository import ResticRepository


def main():
    repository = ResticRepository("mypath", "")
    restic = Restic()
    backup = restic.backup(repository)


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)
    main()
