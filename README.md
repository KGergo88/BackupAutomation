# Backup Automation

Extensible backup automation tool using playbooks.

The project currently only supports the `restic` backend.

## Requirements

- See `pyproject.toml` for the dependencies of this project
- Install the backend you are planning to use:
  - For `restic` playbooks, please install from https://restic.net

## Installation

- Clone the repository and install the package
```bash
$ git clone https://github.com/KGergo88/BackupAutomation.git
$ cd BackupAutomation
$ python -m pip install -e .
```

<em>(The `-e` switch is only needed for development work)</em>

## Usage

Please run the following command for usage information:
```bash
$ backup-automation --help
```

## Playbook format

Playbooks are JSON files. The repository contains example playbooks in the `playbooks` directory.

Playbooks must have a `type` field. This field defines the backend for the playbook. Possible values are: `restic`.

Example:
```json
{
    "type": "restic",
}
```

## Restic playbook format

Restic playbooks are playbooks with the `type` field set to `restic`.

These playbooks must have the following fields: `repositories` and `steps`.

### Repositories

`repositories` list the restic repositories the playbook uses. These can be referenced via their `id` fields.
If the `id` field is missing the `uri` will be used to generate an id value.
For example this repository will have the implicit id `Documents`:
```json
{ "uri": "C:\\ResticBackups\\Documents" }
```

Passwords of the repositories can be provided in the following ways:
- During runtime in the terminal<br>
  If no passwords are provided in the playbook, the program will ask for them.
- Plain text in the playbook<br>
  For this add the `password` field to your repository object with the password:
  `"password": "my_plaintext_password"`
- Via environment variables<br>
  For this add the `password` field to your repository object that
  defines the name of the environment variable that stores the password:
  `"password": "env:MY_RESTIC_PASSWORD_ENV_VAR"`
- Via the prompt credential provider<br>
  For this add the `password` field to your repository object that
  defines the name of the credential that shall be used for the repository:
  `"password": "prompt:my_credential"`
  The program will ask for the password during runtime in the terminal and then store it
  for the duration of the playbook execution. If another repository references the same credential,
  the program will use the stored password and not ask for it again.
  This method is useful if you have multiple repositories that have the same password.
  You can define multiple unique credentials if not all repositories use the same password.

*Note: If the `--no-interaction` switch is active, the program will fail if it needs to ask for a password.*

The program will pass the passwords to the restic backend via temporarily setting environment variables:
- `RESTIC_PASSWORD` — password for the target repository
- `RESTIC_FROM_PASSWORD` — password for the source repository (only for the copy step)

### Steps

`steps` are the sequence of actions the playbook will do upon execution.
Every step has to have a `command` field. Possible values are: `backup`, `copy`.
These represent their matching restic commands: [restic backup][restic-docs-backup] and [restic copy][restic-docs-copy].

#### Backup

With the backup step a path can be backed up to a repository.

The `backup` step needs to have the following fields:
- `repository`: This is a reference to a repository via the repository id
- `source_path`: The path that needs to be backed up to the repository

Optionally the `tags` field can be provided with a list of tags that needs to be applied to the new snapshot.

#### Copy

With the copy step snapshots can be copied between repositories.

The `copy` step needs to have the following fields:
- `source_repository`: Reference to the soruce repository via the repository id
- `target_repository`: Reference to the target repository via the repository id

### Simple example

```json
{
	"type": "restic",
	"repositories": [
		{
            "id": "PC_Documents",
            "uri": "F:\\ResticBackups\\Documents"
        },
        {
            "id": "Raspberry_Documents",
            "uri": "sftp:johndoe@johndoe-raspberry:/media/johndoe/ExternalHdd/ResticBackups/Documents"
        }
	],
	"steps": [
		{
			"command": "backup",
			"repository": "Documents",
			"source_path": "D:\\Documents",
			"tags": ["RegularBackup"]
		},
        {
            "command": "copy",
            "source_repository": "PC_Documents",
            "target_repository": "Raspberry_Documents"
        }
	]
}
```

## Contributing

Contributions and issues are welcome. Open an issue or a pull request on GitHub describing the change. When contributing, prefer small, focused changes and include tests where practical.

## License

See `LICENSE` file.

[restic-docs-backup]: https://restic.readthedocs.io/en/stable/040_backup.html
[restic-docs-copy]: https://restic.readthedocs.io/en/stable/045_working_with_repos.html#copying-snapshots-between-repositories
