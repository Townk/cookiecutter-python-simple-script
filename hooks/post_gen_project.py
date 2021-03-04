"""This module is called after project is created."""

import inspect
import json
import os
import shutil
import subprocess
import sys
import textwrap
from collections import OrderedDict
from pathlib import Path
from subprocess import CompletedProcess
from typing import IO, Callable, List, Mapping, NoReturn, Optional, Sequence

import click
from click import style
from cookiecutter.config import get_user_config

# Template and project information
PROJECT_NAME = "{{ cookiecutter.project.name }}"
PROJECT_DESCRIPTION = "{{ cookiecutter.project.description }}"
PROJECT_SLUG = "{{ cookiecutter.project.slug }}"
PROJECT_VERSION = "{{ cookiecutter.project.version }}"
TEMPLATE_NAME = "{{ cookiecutter._template }}"
REPLAY_DIR = get_user_config().get("replay_dir", "~/.cookiecutter_replay")
FINAL_CONTEXT = dict({{cookiecutter}})

# Licenses values
HAS_LICENSE_DEFINED = {{cookiecutter.license}} is not None
AUTHOR = "{{ cookiecutter.author.name }}"
LICENSE = "{{ cookiecutter.license }}"
# {% if cookiecutter.license %}
LICENSE_KEY = "{{ cookiecutter.license.lice }}"
LICENSE_NAME = "{{ cookiecutter.license.name }}"
# {% else %}
LICENSE_KEY = None
LICENSE_NAME = None
# {% endif %}

# Git and GitHub integration
CREATE_GIT_REPO = {{cookiecutter.repository.enabled}}
PUBLISH_TO_GITHUB = {{cookiecutter.services.github.enabled}}
GITHUB_CLONE_URL = "{{ cookiecutter.services.github.clone_url }}"

# Read the Docs integration
INTEGRATE_READTHEDOCS = {{cookiecutter.services.rtd.enabled}}

DOCS_ARE_MARKDOWN = {{cookiecutter.docs.use_markdown}}


def fail(**kwarg: Mapping[str, str]) -> NoReturn:
    msg_finish_process("error", "red")
    for key, value in kwarg.items():
        key_length = len(key)
        indent = " " * (key_length + 2)
        available_length = click.get_terminal_size()[0] - (key_length + 3)
        click.echo(
            style(f"{key}: ", fg="bright_black")
            + textwrap.fill(
                value,
                width=available_length,
                initial_indent="",
                subsequent_indent=indent,
            )
        )
    exit(1)


def fail_command(result: CompletedProcess) -> NoReturn:
    fail(
        **{
            "Current directory": os.getcwd(),
            "Command": " ".join(result.args),
            "Error code": style(result.returncode, fg="red"),
            "Output": style(result.stderr.strip() or result.stdout, fg="red"),
        }
    )


def run_command(
    *command: str, ignore_failure: Optional[bool] = False
) -> CompletedProcess:
    cmd, *args = command
    cmd_words = cmd.split()
    if len(cmd) > 1:
        command = cmd_words + list(args)
    else:
        command = list(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if not ignore_failure and result.returncode != 0:
        fail_command(result)
    return result


def msg_start_process(verb: str, what: str, target: str):
    click.echo(
        style(f"\n{verb}", bold=True) + f" {what}: " + style(target, fg="cyan"),
        nl=False,
    )


def msg_finish_process(outcome: str, color: Optional[str] = "green"):
    click.echo(f" ({style(outcome, fg=color)})")


def hook_rename_project_dir() -> None:
    current_dir = os.path.abspath(".")
    new_dir = os.path.join(os.path.abspath(".."), "{{ cookiecutter.project.slug }}")
    shutil.move(current_dir, new_dir)
    os.chdir(new_dir)
    if DOCS_ARE_MARKDOWN:
        files = [
            os.path.join(dirpath, filename)
            for dirpath, dirnames, filenames in os.walk(".")
            if dirpath == "."
            or dirpath.startswith("./src")
            or (dirpath.startswith("./docs") and not dirpath.startswith("./docs/_templates"))
            or dirpath.startswith("./tests")
            for filename in filenames
            if filename.endswith(".rst")
        ]
        for f in files:
            shutil.move(f, f[:-3] + "md")


def hook_poetry_install() -> None:
    """Runs `poetry install` on the new project."""
    os.system("poetry install")

    msg_start_process("Updating", "package", "pip")
    run_command("poetry run pip3 install -U pip")
    msg_finish_process("done")


def hook_generate_license() -> None:
    """Generates license file for the project."""
    if HAS_LICENSE_DEFINED:
        msg_start_process("Generating", "license file", LICENSE_NAME)
        result = run_command(
            "lice",
            LICENSE_KEY,
            "-o",
            f"'{AUTHOR}'",
            "-p",
            f"'{PROJECT_NAME}'",
        )
        try:
            with open("LICENSE", "w") as license_file:
                license_file.write(result.stdout)
        except BaseException as ex:
            fail(**{"Error": str(ex)})
        msg_finish_process("done")
    else:
        os.remove("docs/license.{{ cookiecutter.docs.ext }}")


def hook_rtd_integration() -> None:
    """Create the required Read the Docs integration file if user chose
    to integrate with Read the Docs."""
    if not INTEGRATE_READTHEDOCS:
        os.remove(".readthedocs.yaml")


def hook_template_cleanup() -> None:
    """Runs `poetry install` on the new project."""
    os.remove("{{ cookiecutter._context_update_file }}")
    os.remove("__macros.jinja")
    os.remove("__context_update.jinja")

    files = [
        os.path.join(dirpath, filename)
        for dirpath, dirnames, filenames in os.walk(".")
        if dirpath == "."
        or dirpath.startswith("./src")
        or dirpath.startswith("./docs")
        or dirpath.startswith("./tests")
        for filename in filenames
    ]

    msg_start_process("Running", "clean-up hook", "squeeze-empty-lines")
    try:
        for target in files:
            if target.endswith(".rst") or target.endswith(".md") or target == "LICENSE":
                squeeze_empty_lines(target)
    except BaseException as ex:
        fail(**{"Error": str(ex)})
    msg_finish_process("done")
    run_hook("end-of-file-fixer", *files)
    run_hook("trailing-whitespace-fixer", *files)
    run_hook("mixed-line-ending", "--fix=lf", *files)


def run_hook(*args: str) -> None:
    msg_start_process("Running", "clean-up hook", args[0])
    result = run_command("poetry run", *args, ignore_failure=True)
    if not all(
        line.startswith("Fixing") or line.find("fixed mixed") != -1
        for line in result.stdout.splitlines()
    ):
        fail_command(result)
    msg_finish_process("done")


def squeeze_empty_lines(filename: str) -> bool:
    squeezed = False
    if os.path.isfile(filename):
        lines = []
        with open(filename, "r") as input_file:
            current = None
            lookback1 = None
            lookback2 = None
            file_linum = 0

            for line in input_file.readlines():
                file_linum += 1
                lookback2 = lookback1
                lookback1 = current
                current = line.strip()

                # drop all blank lines in the beginning of the file
                if lookback1 is None and not current:
                    current = None
                    continue

                if current:
                    # check if we need to drop the previous blank line if my current line
                    # is a directive's parameter
                    if (
                        lookback2 is not None
                        and not lookback1
                        and lookback2.startswith(".. ")
                        and current.startswith(":")
                    ):
                        lines.pop()
                    # always add non-blank lines
                    lines.append(line)
                    continue

                # keep a blank line after a non-blan line
                if lookback1:
                    lines.append(line)

            squeezed = len(lines) < file_linum

        # drop all blank lines at the end of the file
        while lines and not lines[-1].strip():
            lines.pop()

        if squeezed:
            with open(filename, "w") as output_file:
                output_file.write("".join(lines))
    return squeezed


def hook_git_init() -> None:
    """Initialize Git repository for the project."""
    if CREATE_GIT_REPO:
        msg_start_process("Initializing", "Git repository on branch", "development")
        run_command("git init")
        run_command("git branch -M development")
        run_command("git add .")
        run_command("git commit -m", "🎉 Initial revision")
        run_command(f"git tag v{PROJECT_VERSION}")
        msg_finish_process("done")

        msg_start_process("Installing", "pre-commit hook at", ".git/hooks/pre-commit")
        run_command("poetry run pre-commit install")
        msg_finish_process("done")

        msg_start_process("Building", "initial cached index", "complexity analysis")
        run_command("poetry run poe complexity-build")
        msg_finish_process("done")
    else:
        os.remove("docs/install.{{ cookiecutter.docs.ext }}")
        os.remove(".gitignore")
        os.remove(".pre-commit-config.yaml")


def hook_github_integration() -> None:
    """Create the GitHub repository and connect it to the project's
    repository.

    https://cli.github.com/"""
    if PUBLISH_TO_GITHUB:
        os.system(
            f"gh repo create {PROJECT_SLUG}"
            + " --confirm"
            + " --enable-issues"
            + " --public"
            + f" --description {PROJECT_DESCRIPTION}"
        )
        os.system(f"git remote add origin {GITHUB_CLONE_URL}")


def hook_update_replay_file() -> None:
    if not FINAL_CONTEXT.get("_is_replay", False):
        replay_file = f"{REPLAY_DIR}/{TEMPLATE_NAME}.json"
        if os.path.exists(replay_file):
            msg_start_process("Updating", "Cookiecutter replay file", replay_file)
            _replay = None
            with open(replay_file, "r") as json_file:
                _replay = json.load(json_file)
            _replay["cookiecutter"].update(FINAL_CONTEXT)
            _replay["cookiecutter"]["_is_replay"] = True
            with open(replay_file, "w") as json_file:
                json_file.write(json.dumps(_replay, indent=2, sort_keys=True))
            msg_finish_process("done")


hooks: List[Callable[[], None]] = [
    hook_rename_project_dir,
    hook_poetry_install,
    hook_generate_license,
    hook_rtd_integration,
    hook_template_cleanup,
    hook_git_init,
    # hook_github_integration,
    hook_update_replay_file,
]

click.echo(
    style("\n👷🏗  Start building ", bold=True)
    + style(PROJECT_NAME, fg="cyan")
    + style("'s infrastructure...\n", bold=True)
)

for hook in hooks:
    hook()

click.secho("\nAll done! ✨ 🍰 ✨", bold=True)
