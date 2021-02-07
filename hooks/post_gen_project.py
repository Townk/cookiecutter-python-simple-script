"""This module is called after project is created."""

import os
# import textwrap
from pathlib import Path

# Get the root project directory:
PROJECT_DIRECTORY = Path.cwd().absolute()
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

# We need these values to generate correct license:
LICENSE = "{{ cookiecutter.license }}"
AUTHOR = "{{ cookiecutter.author }}"

# We need these values to generate github repository:
GITHUB_USER = "{{ cookiecutter.github_name }}"

licenses = {
    "MIT": "mit",
    "BSD-3": "bsd3",
    "GNU GPL v3.0": "gpl3",
    "Apache Software License 2.0": "apache",
}


def generate_license() -> None:
    """Generates license file for the project."""
    license_result = os.system(
        f"lice {licenses[LICENSE]} -o '{AUTHOR}' -p '{PROJECT_NAME}' > {PROJECT_DIRECTORY}/LICENSE"
    )
    if license_result:  # it means that return code is not 0, print exception
        print(license_result)


def git_init() -> None:
    """Initialize Git repository for the project."""
    os.system("git init")
    os.system("git branch -M development")
    os.system("git add .")
    os.system("git commit -m '🎉 Initial revision'")
    os.system(f "git remote add origin https://github.com/{GITHUB_USER}/{PROJECT_SLUG}.git")


#def print_futher_instuctions() -> None:
#    """Shows user what to do next after project creation."""
#    message = f"""
#    Your project {PROJECT_NAME} is created.
#    We added the following GitHub repository as your origin:
#
#      https://github.com/{GITHUB_USER}/{PROJECT_SLUG}.git
#
#    1) Now you can start working on it:
#        $ cd {PROJECT_SLUG} && git init
#    2) If you don't have Poetry installed run:
#        $ make download-poetry
#    3) Initialize poetry and install pre-commit hooks:
#        $ make install
#    4) Run codestyle:
#        $ git add . && make install
#    5) Upload initial code to GitHub (ensure you've run `make install` to use `pre-commit`):
#        $ git add .
#        $ git commit -m ":tada: Initial commit"
#        $ git branch -M main
#        $ git remote add origin https://github.com/{GITHUB_USER}/{PROJECT_NAME}.git
#        $ git push -u origin main
#    """
#    print(textwrap.dedent(message))


    if __name__ == "__main__":
    generate_license()
    git_init()
