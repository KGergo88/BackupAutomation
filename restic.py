import logging
import pathlib
import subprocess

from restic_repository import ResticRepository

class Restic:
    def __init__(self):
        logging.info("Looking for restic")
        ret = subprocess.run("restic version", shell=True)
        if ret.returncode != 0:
            raise Exception("Could not find restic! Please install it from https://restic.net")

    def backup(self, repository: ResticRepository):
        logging.info(f"Creating a backup to \"{repository.path}\"")
