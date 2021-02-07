from typing import Callable, List

import re
import sys
import shutil

MODULE_REGEX = r"^[a-z][a-z0-9\-\_]+[a-z0-9]$"
module_name = "{{ cookiecutter._package_name }}"


def validate_project_name() -> None:
    """This validator is used to ensure that `project_name` is valid.
    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or underscores.
    Raises:
        ValueError: If module_name is not a valid Python module name
    """
    if not re.match(MODULE_REGEX, module_name):
        message = f"ERROR: The project name `{module_name}` is not a valid Python module name."

        raise ValueError(message)


def validate_git() -> None:
    if not shutil.which("git"):
        message = "Could not find `git` on your PATH. Make sure you have git installed and " + \
            "its binary on you PATH environment variable."

        raise ValueError(message)


def validate_lice() -> None:
    if not shutil.which("lice6"):
        message = "Could not find `lice6` on your PATH. Make sure you have `lice` installed " + \
            "and its binary on you PATH environment variable."

        raise ValueError(message)


validators: List[Callable[[], None]] = [
    validate_project_name,
    validate_git,
    validate_lice,
]

for validator in validators:
    try:
        validator()
    except ValueError as ex:
        print(ex)
        sys.exit(1)
