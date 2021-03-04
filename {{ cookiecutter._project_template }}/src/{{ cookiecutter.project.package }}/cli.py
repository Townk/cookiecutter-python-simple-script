{#- -*- mode: jinja2; -*- -#}
{%- import "__macros.jinja" as cc with context -%}
"""The command-line interface for {{ cookiecutter.project.name }}.

This module is not for importing on your code. This the entry point of
your application.

{{ cc.doc_section("Todo") }}
{{ "Add the description of your script CLI;" | indent(cc.indent_size if cc.use_google_style else 0) }}
"""

from typing import Any, Union

import click
from click.core import Context, Option, Parameter
from rich.markup import escape

from {{ cookiecutter.project.package }} import __version__, console


def version_callback(context: Context, option: Union[Option, Parameter], value: Any) -> Any:
    """Display the {{ cookiecutter.project.slug }} version and exit.

    This callback is used to implement a custom Version `Click Option`_
    that uses `Rich`_ to display the version information to the user.

    {{ cc.doc_section("Parameters") | indent(cc.indent_size) }}
    {% call cc.doc_param("context") %}
    The ``click`` context passed to the option callback.
    {% endcall %}
    {% call cc.doc_param("option") %}
    The option that trigger this callback. On the normal usage of this callback, this
    argument is always "``-v``" or "``--version``".{% endcall %}

    {% filter indent(cc.indent_size * (2 if cc.use_google_style else 1)) %}
    .. important::
        This parameter is unused in this implementation.
    {% endfilter %}
    {% call cc.doc_param("value") %}
    The value associated with this option. For this
    particular case, it is a boolean indicating if the user has the
    intention to activate or deactivate the flag.
    {% endcall %}

    {{ cc.doc_section("Returns") | indent(cc.indent_size) }}
    {% call cc.doc_return() %}
    Although the callback signature requires the function to
    return `ANY <typing.Any>`, this particular callback always
    returns `None`.{% endcall %}

    .. _Click Option: https://click.palletsprojects.com/en/7.x/options/
    .. _Rich: https://github.com/willmcgugan/rich
    """
    if not value or context.resilient_parsing:
        return

    app_name = "{{ cookiecutter.project.name }}"
    console.print(f"[bold white]{app_name} version:[/] [bold yellow]{__version__}[/]")
    context.exit()


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
    help="Display {{ cookiecutter.project.slug }} version and exit",
)
def {{ cookiecutter.project.package }}() -> None:
    """Offers a set of commands to display greeting messages.

    \f

    {{ cc.doc_section("Todo") }}
    {{ "Add the main function functionality if you add anything to it;" | indent(cc.indent_size if cc.use_google_style else 0) }}
    """
    pass


@{{ cookiecutter.project.package }}.command(options_metavar="<options>")
@click.argument("name", default="World", metavar="<name>")
@click.option("-f", "--formal", is_flag=True, default=False, help="Use a formal form of greeting.")
def hello(name: str, formal: bool = False) -> None:
    """Display a hello greeting text to NAME.

    \f

    {{ cc.doc_section("Parameters") | indent(cc.indent_size) }}
    {% call cc.doc_param("name", cc.role_type("str")) %}
    A single-word name used on the greeting.
    {% endcall %}
    {% call cc.doc_param("formal", cc.role_type("str")) %}
    A flag indicating if the greeting should be a
    formal greeting or not.
    {% endcall %}
    """
    if formal:
        console.print(f"Hello Mr. [bold white]{escape(name)}[/]. Enjoy your day Sir!")
    else:
        console.print(f"Hello [bold white]{escape(name)}[/]!")
