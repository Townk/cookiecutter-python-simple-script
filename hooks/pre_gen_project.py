from typing import Callable, List

import re
import sys
import shutil
import textwrap

MODULE_REGEX = r"^[a-z][a-z0-9\-\_]+[a-z0-9]$"
module_name = "{{ cookiecutter.__project_slug }}"


def validate_project_name() -> None:
    """This validator is used to ensure that `project_name` is valid.
    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or underscores.
    Raises:
        ValueError: If module_name is not a valid Python module name
    """
    if not re.match(MODULE_REGEX, module_name):
        message = f"ERROR: The project name '{module_name}' is not a valid Python module name."

        raise ValueError(message)


def validate_git() -> None:
    if "{{ cookiecutter.create_git_repository }}" == "Yes":
        if not shutil.which("git"):
            message = """You chose to create a git repository for your project, but I could not
                      find the 'git' binary in your PATH.

                      Check the documentation at https://git-scm.com to install 'git' and make sure
                      it's binary is located on a directory listed in your PATH environment
                      variable."""

            raise FileNotFoundError(textwrap.dedent(message))


def validate_lice() -> None:
    if "{{ cookiecutter.license }}" != "None":
        if not shutil.which("lice"):
            message = """You chose to use the {{ cookiecutter.license }} license, but I could not
                      find the 'lice' binary in your PATH.

                      You can install 'lice' with pip:

                          $ pip3 install lice

                      Make sure the directory where pip installs 'lice' is listed in your PATH
                      environment variable."""

            raise FileNotFoundError(textwrap.dedent(message))


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
