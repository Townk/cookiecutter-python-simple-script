{#- -*- mode: jinja2; -*- -#}
"""Sphinx configuration."""

import inspect
import typing
from datetime import datetime

{%- if cookiecutter.docs.use_markdown %}
import myst_parser.docutils_renderer
{%- endif %}

import {{ cookiecutter.project.package }}

#
# -- Project inforrmation -------------------------------------------------
#

project = "{{ cookiecutter.project.name }}"
author = "{{ cookiecutter.author.name }}"
copyright = f"{datetime.now().year}, {author}"


#
# -- General configuration ------------------------------------------------
#

version = "{{ cookiecutter.project.version }}"
release = "{{ cookiecutter.project.version }}"
master_doc = "index"
extensions = [
    {%- if cookiecutter.docs.use_markdown %}
    "myst_parser",
    {%- endif %}
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.duration",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    {%- if cookiecutter.services.github.enabled %}
    "linkcode_resolve",
    {%- endif %}
    {%- if cookiecutter.docs.docstring_style != "Sphinx" %}
    "sphinx.ext.napoleon",
    {%- endif %}
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_click",
    "sphinx_copybutton",
    {%- if cookiecutter.repository.enabled %}
    "sphinx_git",
    {%- endif %}
    "sphinx_inline_tabs",
    "sphinx-prompt",
    "sphinxcontrib.plantuml",
    "sphinxnotes.strike",  # https://sphinx-notes.github.io/strike/
    "scanpydoc.elegant_typehints",
    "scanpydoc.definition_list_typed_field",
    "{{ cookiecutter.docs.theme.extension }}",
]
source_suffix = [".rst"{% if cookiecutter.docs.use_markdown %}, ".md"{% endif %}]
templates_path = ["_templates", "reference/custom"]
default_role = "py:obj"
nitpicky = True
smartquotes = True
add_module_names = False  # Remove namespaces from class/method signatures
pygments_style = "sphinx"


#
# -- Options for autodoc -----------------------------------------------------
#

autoclass_content = "init"  # Add __init__ doc (ie. params) to class summaries
autodoc_inherit_docstrings = False  # If no docstring, inherit from base class
autodoc_default_options = {
    "show-inheritance": True,
}


#
# -- Options for autosectionlabel --------------------------------------------
#

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 3


#
# -- Options for autosummary -------------------------------------------------
#

autosummary_generate = True  # Turn on sphinx.ext.autosummary


#
# -- Options for extlinks ----------------------------------------------------
#

extlinks = {
    {%- if cookiecutter.services.github.enabled %}
    "issue": ("{{ cookiecutter.services.github.url }}/issues/%s", "issue "),
    {%- endif %}
    "pypi": ("https://pypi.org/project/%s/", ""),
}


#
# -- Options for intersphinx -------------------------------------------------
#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "click": ("https://click.palletsprojects.com/en/7.x/", None),
    "rich": ("https://rich.readthedocs.io/en/latest/", None),
}


#
# -- Options for TODOs -------------------------------------------------------
#

todo_include_todos = True


#
# -- Options for type hints --------------------------------------------------
#

typehints_fully_qualified = False
typehints_document_rtype = True
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
always_document_param_types = True
{%- if cookiecutter.docs.use_markdown %}


#
# -- Markdown specific configuration --------------------------------------
#

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
]
myst_heading_anchors = 3
{%- endif %}


#
# -- Options for HTML output ----------------------------------------------
#

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "{{ cookiecutter.docs.theme.extension }}"
html_title = "{{ cookiecutter.project.name }}"
html_show_sourcelink = False  # Remove 'view source code' from top of page (for html, not python)
html_static_path = ["_static"]


#
# -- Options for manual page output ---------------------------------------
#

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, "{{ cookiecutter.project.description }}", [author], 1)]


#
# -- Options for Texinfo output -------------------------------------------
#

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        "{{ cookiecutter.project.description }}",
        "Miscellaneous",
    ),
]
{%- if cookiecutter.docs.docstring_style != "Sphinx" %}


#
# -- Options for Napoleon extension ---------------------------------------
#

napoleon_google_docstring = {{ cookiecutter.docs.docstring_style == "Google" }}
napoleon_numpy_docstring = {{ cookiecutter.docs.docstring_style == "NumPy" }}
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True
napoleon_type_aliases = {
    x: f"typing.{x}"
    for x in typing.__all__
    if type(getattr(typing, x)) == type
    or (
        hasattr(getattr(typing, x), "__module__")
        and getattr(typing, x).__module__ == "typing"
        and not inspect.isfunction(getattr(typing, x))
    )
} | {
    "optional": "*optional*",
    "unused": "*unused*",
}

{%- endif %}



#
# -- Options for ScanPyDoc extension --------------------------------------
#

qualname_overrides = {
    "click.core.Option": "click.Option",
    "click.core.Parameter": "click.Parameter",
    "click.core.Context": "click.Context",
}
