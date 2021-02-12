# -*- coding: utf-8 -*-
"""The command-line interface for {{ cookiecutter.project_name }}.

This module is not for importing on your code. This the entry point of
your application.

Todo
----
* Add the description of your script CLI;

"""

from typing import Any, Union

import click
from click.core import Context, Option, Parameter
from rich.markup import escape

from {{ cookiecutter.__package_name }} import __version__, console


def version_callback(ctx: Context, _: Union[Option, Parameter], value: Any) -> Any:
    """Display the {{ cookiecutter.__project_slug }} version and exit.

    This callback is used to implement a custom Version
    `Click Option <https://click.palletsprojects.com/en/7.x/options/>`_
    that uses `Rich <https://github.com/willmcgugan/rich>`_ to display
    the version information to the user.

    Parameters
    ----------
    ctx : Context
        The `click` context passed to the option callback.
    _ : Option or Parameter
        The option that trigger this callback. On the normal usage of
        this callback, this argument is always "-v" or "--version". This
        parameter is unused on this implementation.
    value : Any
        The value associated with this option. For this particular
        case, it is a boolean indicating if the user has the
        intention to activate or deactivate the flag.

    Returns
    -------
    Any
        This callback always returns None.
    """
    if not value or ctx.resilient_parsing:
        return

    console.print(
        f"[bold white]{{ cookiecutter.project_name }} version:[/] [bold yellow]{__version__}[/]"
    )
    ctx.exit()


@click.group(
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
)
@click.option(
    "-v",
    "--version",
    is_eager=True,
    is_flag=True,
    expose_value=False,
    callback=version_callback,
    help="Display {{ cookiecutter.__project_slug }} version and exit",
)
def {{ cookiecutter.__package_name }}() -> None:
    """Entry point for the {{ cookiecutter.project_name }} application.

    \f # noqa: D205

    Todo
    ----
    * Add the main function functionality if you add anything to it;
    """
    pass


@{{ cookiecutter.__package_name }}.command(options_metavar='<options>')
@click.argument("name", default="World", metavar='<name>')
@click.option("-f", "--formal", default=False, help="Use a formal form of greeting.")
def hello(name: str, formal: bool) -> None:
    """Display a greeting text to NAME.

    \f # noqa: D205

    Parameters
    ----------
    name : str
        A single-word name used on the greeting. (default "World")
    formal : bool
        A flag indicating if the greeting should be a formal greeting or
        not. (default False)
    """
    if formal:
        console.print(f"Hello Mr. [bold white]{escape(name)}[/]. Enjoy your day Sir!")
    else:
        console.print(f"Hello [bold white]{escape(name)}[/]!")


if __name__ == "__main__":
    {{ cookiecutter.__package_name }}()  # pragma: no cover
