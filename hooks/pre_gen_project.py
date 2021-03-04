"""The pre_gen_project file is usually used for validation.

In this cookiecutter, I use it not only to validate if entered or
transformed values are correct, but also if required binaries are
present on the system.

    {{ cookiecutter.update(
        {
            "project": cookiecutter.get("project", {
                "name": cookiecutter.get("Project name", None),
                "slug": None,
                "package": None,
                "description": None,
                "version": None,
            }),
            "author": cookiecutter.get("author", {
                "name": None,
                "email": None,
            }),
            "license": cookiecutter.get("license", None),
            "docs": cookiecutter.get("docs", {
                "use_markdown": False,
                "ext": "rst",
                "theme": {
                    "package": None,
                    "version": None,
                    "extension": None,
                },
                "docstring_style": None,
            }),
            "repository": cookiecutter.get("repository", {
                "enabled": False,
                "type": None,
            }),
            "services": cookiecutter.get("services", {
                "github": {
                    "enabled": False,
                    "username": None,
                    "project_url": None,
                    "project_badge": None,
                    "clone_url": None,
                    "use_actions": False,
                },
                "pypi": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
                "pyversion": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
                "license": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
                "rtd": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
                "tests": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
                "codecov": {
                    "enabled": False,
                    "project_url": None,
                    "project_badge": None,
                },
            }),
        }
    ) }}

These last two structures will change their values depending on how the
user answers some questions from this module.
"""

import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, List, Optional

import arrow
import click
from click import style
from cookiecutter.config import get_user_config
from slugify import slugify


class Config:
    def update(self, obj: dict[str, Any]) -> "Config":
        for attr in dir(self):
            _default_value = getattr(self, attr, None)
            if not callable(_default_value) and not attr.startswith("_"):
                setattr(self, attr, obj.get(attr, _default_value))
        return self

    @classmethod
    def create(cls, obj: dict[str, Any] = None) -> Any:
        return cls().update(obj)


@dataclass(init=False)
class Project(Config):
    name: str = field(default=None)
    description: str = field(default=None)
    version: str = field(default=None)
    slug: str = field(default=None)
    package: str = field(default=None)

    def update(self, obj: dict[str, Any]) -> "Config":
        super().update(obj)
        self._update_names()
        return self

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "name":
            self._update_names()

    def _update_names(self):
        if self.name is not None:
            self.slug = slugify(self.name)
            self.package = self.slug.replace("-", "")


@dataclass(init=False)
class Author(Config):
    name: str = field(default=None)
    email: str = field(default=None)


@dataclass(init=False)
class License(Config):
    name: str = field(default=None)
    lice: str = field(default=None)
    url: str = field(default=None)


LICENSE_OPTIONS = [
    License.create(
        {
            "name": "MIT",
            "lice": "mit",
            "url": "https://opensource.org/licenses/MIT",
        }
    ),
    License.create(
        {
            "name": "BSD-3",
            "lice": "bsd3",
            "url": "https://opensource.org/licenses/BSD-3-Clause",
        }
    ),
    License.create(
        {
            "name": "GNU GPL v3.0",
            "lice": "gpl3",
            "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
        }
    ),
    License.create(
        {
            "name": "Apache Software License 2.0",
            "lice": "apache",
            "url": "https://www.apache.org/licenses/LICENSE-2.0",
        }
    ),
]


@dataclass(init=False)
class Theme(Config):
    name: str = field(default=None)
    package: str = field(default=None)
    version: str = field(default=None)
    extension: str = field(default=None)


DOCS_THEME_OPTIONS = [
    Theme.create(
        {
            "name": "Furo Theme",
            "package": "furo",
            "version": "2020.12.30b24",
            "extension": "furo",
        }
    ),
    Theme.create(
        {
            "name": "Read The Docs Theme",
            "package": "sphinx-rtd-theme",
            "version": "0.5.1",
            "extension": "sphinx_rtd_theme",
        }
    ),
    Theme.create(
        {
            "name": "Sphinx Readable Them",
            "package": "sphinx-readable-theme",
            "version": "1.1.0",
            "extension": "readable",
        }
    ),
    Theme.create(
        {
            "name": "Sphinx Book Theme",
            "package": "sphinx-book-theme",
            "version": "0.0.39",
            "extension": "sphinx_book_theme",
        }
    ),
    Theme.create(
        {
            "name": "PyData Sphinx Theme",
            "package": "pydata-sphinx-theme",
            "version": "0.4.3",
            "extension": "pydata_sphinx_theme",
        }
    ),
    Theme.create(
        {
            "name": "Material Sphinx Theme",
            "package": "sphinx-material",
            "version": "0.0.32",
            "extension": "sphinx_material",
        }
    ),
]


@dataclass(init=False)
class Docs:
    use_markdown: str = field()
    docstring_style: str = field()
    ext: str = field()
    theme: Theme = field()

    def __init__(self):
        self.use_markdown: str = "{{ cookiecutter.docs.use_markdown }}"
        self.docstring_style: str = "{{ cookiecutter.docs.docstring_style }}"
        self.ext: str = "{{ cookiecutter.docs.ext }}"
        self.theme: Theme = Theme.create({{cookiecutter.docs.theme}})


@dataclass(init=False)
class Integration(Config):
    enabled: bool = field(default=False)


@dataclass(init=False)
class Repository(Integration):
    type: Optional[str] = field(default=None)


@dataclass(init=False)
class Service(Integration):
    project_url: Optional[str] = field(default=None)
    project_badge: Optional[str] = field(default=None)


@dataclass(init=False)
class GitHubService(Service):
    username: Optional[str] = field(default=None)
    clone_url: Optional[str] = field(default=None)
    use_actions: bool = field(default=False)


@dataclass(init=False)
class Services:
    github: GitHubService = field()
    pypi: Service = field()
    pyversion: Service = field()
    license: Service = field()
    rtd: Service = field()
    tests: Service = field()
    codecov: Service = field()

    def __init__(self):
        self.github: GitHubService = GitHubService.create(
            {{cookiecutter.services.github}}
        )
        self.pypi: Service = Service.create({{cookiecutter.services.pypi}})
        self.pyversion: Service = Service.create({{cookiecutter.services.pyversion}})
        self.license: Service = Service.create({{cookiecutter.services.license}})
        self.rtd: Service = Service.create({{cookiecutter.services.rtd}})
        self.tests: Service = Service.create({{cookiecutter.services.tests}})
        self.codecov: Service = Service.create({{cookiecutter.services.codecov}})


_NOW = arrow.now("local")


@dataclass(init=False)
class ExtraContext:
    project: Project = field()
    author: Author = field()
    license: License = field()
    docs: Docs = field()
    repository: Repository = field()
    services: Services = field()
    _is_replay: bool = field()
    _context_update_file: str = field()
    _date: arrow.Arrow = field()
    _date_short: arrow.Arrow = field()
    _date_full: arrow.Arrow = field()
    _project_template: str = field()

    def __init__(self):
        self.project: Project = Project.create({{cookiecutter.project}})
        self.author: Author = Author.create({{cookiecutter.author}})
        _license_default = {{cookiecutter.license}}
        self.license: License = (
            None if _license_default is None else License.create(_license_default)
        )
        self.docs: Docs = Docs()
        self.repository: Repository = Repository.create({{cookiecutter.repository}})
        self.services: Services = Services()
        self._is_replay: bool = {{cookiecutter.get("_is_replay", False)}}
        self._context_update_file: str = None
        self._date: arrow.Arrow = _NOW.strftime("%b %-d %Y")
        self._date_short: arrow.Arrow = _NOW.strftime("%Y-%m-%d")
        self._date_full: arrow.Arrow = _NOW.strftime("%A, %B %-d %Y")
        self._project_template = self.project.slug


UPDATES = ExtraContext()
CC_USER_CONFIG = get_user_config()

# % user, project-slug
GITHUB_URL = "https://github.com/%s/%s"
# % user, project-slug
GITHUB_BADGE = (
    "https://img.shields.io/github/v/release/%s/%s?"
    + "include_prereleases&logo=github&logoColor=%%23f5f5f5&sort=semver"
)
# % user, project-slug
GITHUB_CLONE_URL = "git@github.com:%s/%s"
# % user, project-slug
GITHUB_TEST_ACTION = "https://github.com/%s/%s/actions?workflow=Tests"
# % user, project-slug
GITHUB_TEST_ACTION_BADGE = "https://github.com/%s/%s/workflows/Tests/badge.svg"
# % user, project-slug
CODECOV_URL = "https://codecov.io/gh/%s/%s"
# % user, project-slug
CODECOV_BADGE = "https://codecov.io/gh/%s/%s/branch/master/graph/badge.svg"
# % project-slug
PYPI_URL = "https://pypi.org/project/%s"
# % project-slug
PYPI_BADGE = (
    "https://img.shields.io/pypi/v/%s?label=Release&logo=pypi&logoColor=%%23f5f5f5"
)
# % project-slug
PYPI_PYVERSION_BADGE = (
    "https://img.shields.io/pypi/pyversions/%s?logo=pypi&logoColor=%%23f5f5f5"
)
# % project-slug
PYPI_LICENSE_BADGE = "https://img.shields.io/pypi/l/%s?logo=pypi&logoColor=%%23f5f5f5"
# % project-slug
RTD_URL = "https://%s.readthedocs.io/"
# % project-slug
RTD_BADGE = "https://img.shields.io/readthedocs/%s/latest.svg?label=Read%%20the%%20Docs"

_QUESTION_COUNTER = 1

CHAR_UP = "\x1b[A"
CHAR_DOWN = "\x1b[B"


def move_line_up(count: int=1):
    sys.stdout.write("\033[F" * count)
    sys.stdout.flush()


def question_header(
    question: str, default: Optional[str] = None, mandatory: bool = False
) -> None:
    global _QUESTION_COUNTER
    qnum = f"{_QUESTION_COUNTER}.".rjust(3, " ")
    length = len(qnum)
    _QUESTION_COUNTER += 1
    if default is None and mandatory:
        default_answer = style("mandatory question", fg="cyan")
    else:
        default_answer = (
            ""
            if default is None
            else style(f"default='", fg="bright_black")
            + style(default, fg="cyan")
            + style("'", fg="bright_black")
        )
    click.echo("\n┌─" + ("─" * length) + "─┬" + ("─" * (72 - (length + 5))))
    click.echo(f"│ {style(qnum, fg='yellow')} │ {style(question, fg='bright_white')}")
    click.echo("└─" + ("─" * length) + "─┘ " + default_answer)


def format_option(num: int, name: str, default: Optional[int] = None) -> None:
    if num == default:
        click.echo(f"{style('─▶', fg='green')} {style(f'{num}. {name}', bold=True)}")
    else:
        click.echo(f"   {num}. {name}")


def format_options(options: List[str], default: Optional[int] = None) -> None:
    for num, name in enumerate(options, 1):
        format_option(num, name, default)


def read_free_text(text: str, default: Optional[str] = None) -> str:
    question_header(text, default, default is None)
    answer = None
    click.echo("\n")
    while True:
        click.echo(f"   {style('A.', fg='green')} : ", nl=False)
        if answer is not None:
            break
        answer = click.prompt(
            "",
            default=default or "",
            show_default=False,
            prompt_suffix="",
        ).strip()
        if default is not None or answer:
            move_line_up()
            continue
        click.echo(f"{style('Invalid entry!', fg='red')} This question is mandatory!", nl=False)
        move_line_up()
        answer = None
    click.secho(answer, fg="green")
    click.echo(" " * 72)
    move_line_up()
    return answer


def read_options(text: str, options: List[str], default: Optional[int] = None) -> int:
    question_header(text, None if default is None else str(default))
    click.echo(" ")
    format_options(options, default)
    click.echo(" ")
    options_count = len(options)
    opt = None
    while True:
        click.echo(
            f"   {style('A.', fg='green')} Choose between '{style('1', fg='bright_white')}' "
            + f"and '{style(str(len(options)), fg='bright_white')}': ",
            nl=False,
        )
        if opt is not None:
            break
        opt = click.getchar(echo=False)
        if opt == "\r" and default is not None:
            opt = default
            break
        if opt.isnumeric():
            opt = int(opt)
            if opt >= 1 and opt <= options_count:
                move_line_up(options_count + 1)
                format_options(options, opt)
                click.echo(" ")
                continue
        if opt in (CHAR_UP, CHAR_DOWN, "j", "J", "k", "K", "n", "N", "p", "P"):
            if opt in (CHAR_UP, "k", "K", "p", "P"):
                default = 0 if default is None else max(default - 1, 1)
            else:
                default = 0 if default is None else min(default + 1, options_count)
            move_line_up(options_count + 1)
            format_options(options, default)
            click.echo(" ")
            opt = None
            continue
        if not isinstance(opt, int) and not opt.isprintable():
            # opt = ",".join([hex(ord(x)) for x in opt])
            opt = repr(opt)
        else:
            opt = f"'{opt}'"
        click.secho(f"   ({opt} is an invalid option!)" + " " * 13, fg="red", nl=False)
        move_line_up()
        click.echo("")
        opt = None
    success_text = f"{opt} ({options[opt-1]})"
    success_text_size = len(success_text)
    click.secho(success_text, fg="green", nl=False)
    click.echo(" " * max(0, 45 - success_text_size))
    return opt


def read_yes_no(text: str, default: Optional[bool] = None) -> bool:
    question_header(
        text,
        None
        if default is None
        else style("y", underline=True, fg="cyan") + style("es", fg="cyan")
        if default
        else style("n", underline=True, fg="cyan") + style("o", fg="cyan"),
    )
    click.echo("\n")
    opt = None
    while True:
        click.echo(
            f"   {style('A.', fg='green')} "
            + f"'{style('y', underline=True)}es' or '{style('n', underline=True)}o'? ",
            nl=False,
        )
        opt = click.getchar(echo=False)
        if opt == "\r" and default is not None:
            opt = default
            break
        if opt.lower() in ("y", "n", "1", "0"):
            opt = opt.lower() == "y" or opt == "1"
            break

        if not opt.isprintable():
            opt = repr(opt)
        else:
            opt = f"'{opt}'"
        click.echo(
            style(f"   ({opt} is an invalid option! ", fg="red")
            + style(f"Press '", fg="red")
            + style("y", fg="bright_white")
            + style(f"' or '", fg="red")
            + style("n", fg="bright_white")
            + style(f"' to answer the question.)", fg="red") + " " * 5,
            nl=False)
        move_line_up()
        click.echo("")
        opt = None
    click.secho(f"{'Yes' if opt else 'No'}", fg="green", nl=False)
    click.echo(" " * 74)
    return opt


def validate_poetry() -> None:
    """Ensure `poetry` is installed on the machine before proceeding.

    Raises
    ------
    FileNotFoundError
        If the ``poetry`` binary is not present.
    """
    if not shutil.which("poetry"):
        message = """This cookiecutter uses Poetry as its dependency manager, but I could not
                  find the 'poetry' binary in your PATH.

                  Check the documentation at https://python-poetry.org/docs to install 'poetry'
                  and make sure it's binary is located on a directory listed in your PATH
                  environment variable."""

        raise FileNotFoundError(textwrap.dedent(message))


def read_and_validate_extra_info():
    _open = "{"
    _close = "}"
    _template_dir = "{{ cookiecutter._output_dir ~ '/' ~ cookiecutter._template }}"
    _template_proj_dir = (
        f"{_open}{_open} cookiecutter._project_template {_close}{_close}"
    )
    _ctx_update_file = os.path.realpath(
        f"{_template_dir}/{_template_proj_dir}/__context_update.jinja"
    )
    _ctx_update_expression = f"{_open}{_open} cookiecutter.update(%s) {_close}{_close}"
    if not UPDATES._is_replay:
        read_and_validate_project_name()
        read_and_validate_project_description()
        read_and_validate_project_initial_version()
        read_and_validate_author()
        read_and_validate_license()
        read_and_validate_markup_language()
        read_and_validate_docs_theme()
        read_and_validate_docstring_style()
        read_and_validate_git_usage()
        UPDATES._context_update_file = _ctx_update_file
        with open(_ctx_update_file, "w") as updater:
            updater.write(_ctx_update_expression % asdict(UPDATES).__repr__())
    else:
        with open(_ctx_update_file, "w") as updater:
            updater.write("{# Nothing to update #}")


def read_and_validate_project_name():
    UPDATES.project.name = read_free_text(
        "What is the name of your project?",
        default="Awesome Project",
    )
    UPDATES._project_template = UPDATES.project.slug


def read_and_validate_project_description():
    UPDATES.project.description = read_free_text(
        "What is the one-line summary description for your new project?",
        default="Simple Python script",
    )


def read_and_validate_project_initial_version():
    UPDATES.project.version = read_free_text(
        "What is the initial version of your project?",
        default="0.0.1",
    )


def read_and_validate_author():
    _author_name = CC_USER_CONFIG.get(
        "author",
        CC_USER_CONFIG["default_context"].get(
            "author", os.getenv("USER_FULL_NAME") or "Author Name"
        ),
    )
    _author_email = CC_USER_CONFIG.get(
        "email",
        CC_USER_CONFIG["default_context"].get(
            "author_email", os.getenv("USER_EMAIL") or "author@email.com"
        ),
    )
    UPDATES.author.name = read_free_text(
        "What is the project author's name?",
        default=_author_name,
    )
    UPDATES.author.email = read_free_text(
        "What is the project author's email?",
        default=_author_email,
    )


def read_and_validate_license():
    choice = (
        read_options(
            text="What license do you want to use on your project?",
            options=["No Open Source license"] + [opt.name for opt in LICENSE_OPTIONS],
            default=2,
        )
        - 2
    )

    if choice >= 0:
        validate_lice()
        UPDATES.license = LICENSE_OPTIONS[choice]
        UPDATES.services.license.enabled = True


def validate_lice() -> None:
    """Ensure lice is installed on the machine before proceeding.

    Raises
    ------
    FileNotFoundError
        If the lice binary is not present.
    """
    if not shutil.which("lice"):
        message = """You chose to use the {{ cookiecutter.license }} license, but I could not
                    find the 'lice' binary in your PATH.

                    You can install 'lice' with pip:

                        $ pip3 install lice

                    Make sure the directory where pip installs 'lice' is listed in your PATH
                    environment variable."""

        raise FileNotFoundError(textwrap.dedent(message))


def read_and_validate_markup_language():
    choice = read_options(
        text="Which markup language do you want to use for documentation?",
        options=["Markdown", "reStructuredText"],
        default=1,
    )
    UPDATES.docs.use_markdown = choice == 1
    UPDATES.docs.ext = "md" if UPDATES.docs.use_markdown else "rst"


def read_and_validate_docs_theme():
    choice = (
        read_options(
            text="What HTML theme do you want to use on your documentation?",
            options=[opt.name for opt in DOCS_THEME_OPTIONS],
            default=1,
        )
        - 1
    )
    UPDATES.docs.theme = DOCS_THEME_OPTIONS[choice]


def read_and_validate_docstring_style():
    styles = ["Google", "NumPy", "Sphinx"]
    choice = (
        read_options(
            text="What Docstring style do you like to use?",
            options=styles,
            default=1,
        )
        - 1
    )
    UPDATES.docs.docstring_style = styles[choice]


def read_and_validate_git_usage() -> None:
    UPDATES.repository.enabled = read_yes_no(
        "Would you like to crate a Git repository for this project?",
        default=False,
    )

    if UPDATES.repository.enabled:
        validate_git()
        UPDATES.repository.type = "git"
        read_and_validate_github_usage()


def validate_git() -> None:
    """Ensure git is installed on the machine before proceeding.

    Raises
    ------
    FileNotFoundError
        If the git binary is not present.
    """
    if not shutil.which("git"):
        message = """You chose to create a git repository for your project, but I could not
                  find the 'git' binary in your PATH.

                  Check the documentation at https://git-scm.com to install 'git' and make sure
                  it's binary is located on a directory listed in your PATH environment
                  variable."""

        raise FileNotFoundError(textwrap.dedent(message))


def read_and_validate_github_usage() -> None:
    UPDATES.services.github.enabled = read_yes_no(
        "Would you like to publish this project on GitHub?",
        default=False,
    )

    if UPDATES.services.github.enabled:
        validate_github_cli()
        read_and_validate_github_user()
        read_and_validate_github_use_actions()

        UPDATES.services.github.project_url = GITHUB_URL % (
            UPDATES.services.github.username,
            UPDATES.project.slug,
        )
        UPDATES.services.github.project_badge = GITHUB_BADGE % (
            UPDATES.services.github.username,
            UPDATES.project.slug,
        )
        UPDATES.services.github.clone_url = GITHUB_CLONE_URL % (
            UPDATES.services.github.username,
            UPDATES.project.slug,
        )

        if UPDATES.services.github.use_actions:
            UPDATES.services.tests.enabled = True
            UPDATES.services.tests.project_url = GITHUB_TEST_ACTION % (
                UPDATES.services.github.username,
                UPDATES.project.slug,
            )
            UPDATES.services.tests.project_badge = GITHUB_TEST_ACTION_BADGE % (
                UPDATES.services.github.username,
                UPDATES.project.slug,
            )

        if UPDATES.license is not None:
            UPDATES.services.license.project_url = UPDATES.license.url
        UPDATES.services.license.project_badge = UPDATES.services.github.project_badge

        read_and_validate_codecov_usage()
        read_and_validate_pypi_usage()
        read_and_validate_rtd_usage()


def validate_github_cli() -> None:
    """Ensure ``gh`` is installed on the machine before proceeding.

    Raises
    ------
    FileNotFoundError
        If the ``gh`` binary is not present.
    ChildProcessError
        If ``gh auth status`` fails.
    """
    if not shutil.which("gh"):
        message = """You chose to publish the repository into GitHub, but I could not
                  find the GitHub cli (gh) binary in your PATH.

                  Check the documentation at https://cli.github.com to install 'gh' and
                  make sure it's binary is located on a directory listed in your PATH
                  environment variable."""

        raise FileNotFoundError(textwrap.dedent(message))

    _gh_result = subprocess.run(
        ["gh", "auth", "status"], capture_output=True, text=True
    )

    if _gh_result.returncode != 0:
        message = f"""Could not verify authentication with GitHub. `gh` exited with code
                   {_gh_result.returncode}, and the following error:

                   {_gh_result.stderr}

                   Make sure your GitHub token is valid and has the correct permissions to
                   create a new repository.

                   according to the GitHub CLI documentation:

                   > Run `gh auth login` to authenticate with your GitHub account. `gh` will
                   > respect tokens set using `GITHUB_TOKEN`."""
        raise ChildProcessError(textwrap.dedent(message))


def read_and_validate_github_user() -> None:
    _github_user = subprocess.run(
        ["git", "config", "github.user"], capture_output=True, text=True
    )
    _github_user = (
        _github_user.stdout.strip()
        if _github_user.returncode == 0
        else (
            os.getenv("GITHUB_USERNAME")
            or os.getenv("USERNAME")
            or os.getenv("USER")
            or None
        )
    )

    UPDATES.services.github.username = read_free_text(
        "What is your GitHub username?",
        default=_github_user,
    )


def read_and_validate_github_use_actions() -> None:
    UPDATES.repository.use_actions = read_yes_no(
        "Would you like to integrate with GitHub Actions?",
        default=True,
    )


def read_and_validate_codecov_usage() -> None:
    UPDATES.services.codecov.enabled = read_yes_no(
        "Would you like to use CodCov to monitor your tests coverage?",
        default=True,
    )

    if UPDATES.services.codecov.enabled:
        UPDATES.services.codecov.project_url = CODECOV_URL % (
            UPDATES.services.github.username,
            UPDATES.project.slug,
        )
        UPDATES.services.codecov.project_badge = CODECOV_BADGE % (
            UPDATES.services.github.username,
            UPDATES.project.slug,
        )


def read_and_validate_pypi_usage() -> None:
    UPDATES.services.pyversion.enabled = UPDATES.services.pypi.enabled = read_yes_no(
        "Would you like to publish your projet to PyPI?",
        default=True,
    )

    if UPDATES.services.pypi.enabled:
        UPDATES.services.pypi.project_url = PYPI_URL % UPDATES.project.slug
        UPDATES.services.pypi.project_badge = PYPI_BADGE % UPDATES.project.slug
        UPDATES.services.pyversion.project_url = UPDATES.services.pypi.project_url
        UPDATES.services.pyversion.project_badge = (
            PYPI_PYVERSION_BADGE % UPDATES.project.slug
        )

        if UPDATES.license is not None:
            UPDATES.services.license.project_badge = (
                PYPI_LICENSE_BADGE % UPDATES.project.slug
            )


def read_and_validate_rtd_usage() -> None:
    UPDATES.services.rtd.enabled = read_yes_no(
        "Would you like to publish your projet's documentation to Read the Docs?",
        default=True,
    )

    if UPDATES.services.rtd.enabled:
        UPDATES.services.rtd.project_url = RTD_URL % UPDATES.project.slug
        UPDATES.services.rtd.project_badge = RTD_BADGE % UPDATES.project.slug


validators: List[Callable[[], None]] = [
    validate_lice,
    validate_poetry,
    read_and_validate_extra_info,
]

for validator in validators:
    try:
        validator()
    except (ValueError, FileNotFoundError, ChildProcessError) as ex:
        print(ex)
        sys.exit(1)
