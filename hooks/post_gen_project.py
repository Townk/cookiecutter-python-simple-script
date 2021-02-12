"""This module is called after project is created."""

from pathlib import Path
from typing import Callable
from typing import List

import inspect
import os
import sys
import shutil
import textwrap

# Get the root project directory:
PROJECT_DIRECTORY = Path.cwd().absolute()
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_DESCRIPTION = "{{ cookiecutter.project_description }}"
PROJECT_SLUG = "{{ cookiecutter.__project_slug }}"

# Licenses values
HAS_LICENSE_DEFINED = "{{ cookiecutter.license }}" != "None"
AUTHOR = "{{ cookiecutter.author }}"
LICENSE = "{{ cookiecutter.license }}"
LICENSE_KEY = "{{ None if cookiecutter.license == 'None' else cookiecutter._licenses[cookiecutter.license].lice }}"
TRIM_CMD = ""
FINAL_EMPTY_LINE_CMD = ""
if sys.platform == "darwin":
    if shutil.which("gsed"):
        FINAL_EMPTY_LINE_CMD = "gsed -i -e :a -e '/^\\n*$/{$d;N;ba' -e '}' \"%s\""
        TRIM_CMD = "gsed -i 's/[ \t]*$//' \"{0}\""
    else:
        FINAL_EMPTY_LINE_CMD = "sed -i '' -e :a -e '/^\\n*$/{$d;N;ba' -e '}' \"%s\""
        TRIM_CMD = "sed -i '' -E 's/[ '$'\t'']+$//' \"{0}\""
else:
    FINAL_EMPTY_LINE_CMD = "sed -i -e :a -e '/^\\n*$/{$d;N;ba' -e '}' \"%s\""
    TRIM_CMD = "sed -i 's/[ \t]*$//' \"{0}\""

# Git and GitHub integration
CREATE_GIT_REPO = "{{ cookiecutter.create_git_repository }}" == "Yes"
PUBLISH_TO_GITHUB = "{{ cookiecutter.__use_github }}" == "True"
GITHUB_USER = "{{ cookiecutter.github_user }}"

# Read the Docs integration
INTEGRATE_READTHEDOCS = "{{ cookiecutter.__use_readthedocs }}" == "True"


def hook_generate_license() -> None:
    """Generates license file for the project."""
    if HAS_LICENSE_DEFINED:
        license_result = os.system(
            f"lice {LICENSE_KEY} -o '{AUTHOR}' -p '{PROJECT_NAME}' > {PROJECT_DIRECTORY}/LICENSE"
        )
        if license_result:  # it means that return code is not 0, print exception
            print(license_result)
        else:
            os.system(TRIM_CMD.format(f"{PROJECT_DIRECTORY}/LICENSE"))
            os.system(FINAL_EMPTY_LINE_CMD % f"{PROJECT_DIRECTORY}/LICENSE")
    else:
        os.remove("docs/license.{{ cookiecutter.__doc_ext }}")


def hook_git_init() -> None:
    """Initialize Git repository for the project."""
    if CREATE_GIT_REPO:
        os.system("git init")
        os.system("git branch -M development")
        os.system("git add .")
        os.system("git commit -m '🎉 Initial revision'")
        os.system("poetry run pre-commit install")
    else:
        os.remove(".gitignore")
        os.remove(".pre-commit-config.yaml")


def hook_github_integration() -> None:
    """Create the GitHub repository and connect it to the project's
    repository.

    https://cli.github.com/"""
    if PUBLISH_TO_GITHUB:
        os.system(f"gh repo create {PROJECT_SLUG}" +
                  f" --confirm" +
                  f" --enable-issues" +
                  f" --public" +
                  f" --description {PROJECT_DESCRIPTION}")
        os.system(f"git remote add origin https://github.com/{GITHUB_USER}/{PROJECT_SLUG}.git")


def hook_rtd_integration() -> None:
    """Create the required Read the Docs integration file if user chose
    to integrate with Read the Docs."""
    if not INTEGRATE_READTHEDOCS:
        os.remove(".readthedocs.yaml")


def hook_poetry_install() -> None:
    """Runs `poetry install` on the new project."""
    os.system("poetry install")
    os.system("poetry run pip3 install -U pip")
    os.system(FINAL_EMPTY_LINE_CMD % f"{PROJECT_DIRECTORY}/docs/conf.py")
    # os.system("poetry run task style")


hooks: List[Callable[[], None]] = [
    hook_generate_license,
    hook_rtd_integration,
    hook_poetry_install,
    hook_git_init,
    hook_github_integration,
]

for hook in hooks:
    hook()
