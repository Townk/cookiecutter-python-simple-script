{#- -*- mode: jinja2; -*- -#}
{%- import "__macros.jinja" as cc with context -%}
"""{{ cookiecutter.project.description }}.

The {{ cookiecutter.project.package }} package is the main package for the
{{ cookiecutter.project.name }} script.

{{ cc.doc_section("Note") }}
{% call cc.indent_block(1 if cc.use_google_style else 0, text_width=72 if cc.use_md else (72 - cc.indent_size)) %}
We use the `Rich`_ library to output information on the script, the
the main object we use is the attribute ``console`` from this module.
For applications that make use of logging from Python standard
library, this module also installs the `Rich`_ log handler into
Python's logging framework, so normal logging goes through
`Rich`_ as well.
{% endcall %}

.. _Rich: https://github.com/willmcgugan/rich
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

#! The script's semantic version.
#!
#! If you need to use Awesome Script's version, this is the constant you
#! should use for such task.
__version__: str = "{{ cookiecutter.project.version }}"

#: The main object to output information on the script.
#:
#: You can use this constant as a {{ cc.role("print", name="func") }} wrapper to send text to
#: ``stdout`` or ``stderr``.
console: Console = Console()

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S.%f (%z)]",
    handlers=[
        RichHandler(
            console=console,
            rich_tracebacks=True,
        )
    ]
)
