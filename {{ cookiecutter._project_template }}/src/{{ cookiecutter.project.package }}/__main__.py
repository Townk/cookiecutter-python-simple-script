{#- -*- mode: jinja2; -*- -#}
{%- import "__macros.jinja" as cc with context -%}
"""{% call cc.indent_block(0, text_width=72) %}The __main__ module for {{ cookiecutter.project.name }}.

This allows one to invoke {{ cookiecutter.project.name }} using the
``-m`` flag with ``python``, for instance
{% endcall %}

.. prompt: bash $ auto

    $ python -m {{ cookiecutter.project.package }}

"""

from {{ cookiecutter.project.package }} import cli


if __name__ == "__main__":
    cli.{{ cookiecutter.project.package }}()  # pragma: no cover
