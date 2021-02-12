"""The pre_gen_project is usually used for validation.

In this cookiecutter, we use it not only to validate if entered or
transformed values are correct, but also if required binaries are
present on the system.
"""

from typing import Callable
from typing import List

import inspect
import re
import sys
import shutil
import textwrap
import os


# Package name validation
MODULE_REGEX = r"^[a-z][a-z0-9\-\_]+[a-z0-9]$"
MODULE_NAME = "{{ cookiecutter.__project_slug }}"

# Git and GitHub integration
CREATE_GIT_REPO = "{{ cookiecutter.__use_git }}" == "y"
PUBLISH_TO_GITHUB = "{{ cookiecutter.__use_github }}" == "y"

# Licenses values
HAS_LICENSE_DEFINED = "{{ cookiecutter.license }}" != "None"


def validate_project_name() -> None:
    """Ensure that `package_name` is valid Python package name.

    Valid inputs starts with the lowercase letter, followed by any
    lowercase letters, numbers or underscores.

    Raises:
        ValueError: If MODULE_NAME is not a valid Python module name
    """
    if not re.match(MODULE_REGEX, MODULE_NAME):
        message = f"ERROR: The project name '{MODULE_NAME}' is not a valid Python module name."

        raise ValueError(message)


def validate_git() -> None:
    """Ensure git is installed on the machine before proceeding.

    Raises:
        FileNotFoundError: If the git binary is not present.
    """
    if CREATE_GIT_REPO:
        if not shutil.which("git"):
            message = """You chose to create a git repository for your project, but I could not
                      find the 'git' binary in your PATH.

                      Check the documentation at https://git-scm.com to install 'git' and make sure
                      it's binary is located on a directory listed in your PATH environment
                      variable."""

            raise FileNotFoundError(textwrap.dedent(message))


def validate_lice() -> None:
    """Ensure lice is installed on the machine before proceeding.

    Raises:
        FileNotFoundError: If the lice binary is not present.
    """
    if HAS_LICENSE_DEFINED:
        if not shutil.which("lice"):
            message = """You chose to use the {{ cookiecutter.license }} license, but I could not
                      find the 'lice' binary in your PATH.

                      You can install 'lice' with pip:

                          $ pip3 install lice

                      Make sure the directory where pip installs 'lice' is listed in your PATH
                      environment variable."""

            raise FileNotFoundError(textwrap.dedent(message))
        if not shutil.which("gsed") or not shutil.which("sed"):
            message = """You chose to use the {{ cookiecutter.license }} license, but I could not
                      find 'sed' or 'gsed' binary in your PATH.

                      I need 'sed' to cleanup whitespaces from the licence file created by 'lice'.

                      Make sure you have 'sed' or 'gsed' installed on your system."""

            raise FileNotFoundError(textwrap.dedent(message))
    pass


def validate_github_cli() -> None:
    """Ensure `gh` is installed on the machine before proceeding.

    Raises:
        FileNotFoundError: If the `gh` binary is not present.
        ChildProcessError: If `gh auth status` fails.
    """
    if CREATE_GIT_REPO and PUBLISH_TO_GITHUB:
        if not shutil.which("gh"):
            message = """You chose to publish the repository into GitHub, but I could not
                      find the GitHub cli (gh) binary in your PATH.

                      Check the documentation at https://cli.github.com to install 'gh' and
                      make sure it's binary is located on a directory listed in your PATH
                      environment variable."""

            raise FileNotFoundError(textwrap.dedent(message))

        gh_status_result = os.system("gh auth status")
        if gh_status_result:  # it means that return code is not 0, raise an exception
            message = f"""Could not verify authentication with GitHub. `gh` returned the following
                       error:

                       {gh_status_result}

                       Make sure your GitHub token is valid and has the correct permissions to
                       create a new repository.

                       according to the GitHub CLI documentation:

                       > Run `gh auth login` to authenticate with your GitHub account. `gh` will
                       > respect tokens set using `GITHUB_TOKEN`."""
            raise ChildProcessError(textwrap.dedent(message))


def validate_poetry() -> None:
    """Ensure `poetry` is installed on the machine before proceeding.

    Raises:
        FileNotFoundError: If the `poetry` binary is not present.
    """
    if not shutil.which("poetry"):
        message = """This cookiecutter uses Poetry as its dependency manager, but I could not
                  find the 'poetry' binary in your PATH.

                  Check the documentation at https://python-poetry.org/docs to install 'poetry'
                  and make sure it's binary is located on a directory listed in your PATH
                  environment variable."""

        raise FileNotFoundError(textwrap.dedent(message))


validators: List[Callable[[], None]] = [
    obj for name, obj in inspect.getmembers(sys.modules[__name__])
    if (inspect.isfunction(obj) and name.startswith("validate_"))]

for validator in validators:
    try:
        validator()
    except (ValueError, FileNotFoundError, ChildProcessError) as ex:
        print(ex)
        sys.exit(1)
