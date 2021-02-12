# -*- coding: utf-8 -*-
"""{{ cookiecutter.project_description }}.

The {{ cookiecutter.__package_name }} package is the main package for the
{{ cookiecutter.project_name }} script.

Attributes
----------
__version__ : str
    The script's semantic version.

console : Console
    The main object to output information on the script.

Notes
-----
We use the `Rich`_ library to output information on the script, the the
main object we use is the attribute `console` from this module.

This module also installs the `Rich`_ log handler into Python's logging
framework, so normal logging goes through `Rich`_ as well.

.. _Rich:
   https://github.com/willmcgugan/rich
"""

import logging

from rich.console import Console
from rich.logging import RichHandler

__version__ = "{{ cookiecutter.version }}"

console = Console()

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
