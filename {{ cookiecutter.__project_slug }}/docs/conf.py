"""Sphinx configuration."""
from datetime import datetime
{%- if cookiecutter.__use_markdown == "True" %}
from recommonmark.transform import AutoStructify

import recommonmark
{%- endif %}

# -- Project inforrmation -------------------------------------------------

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author }}"
copyright = f"{datetime.now().year}, {author}"


# -- Base Sphinx configuration --------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_click",
    "sphinx_rtd_theme",
    {%- if cookiecutter.__use_markdown == "True" %}
    "recommonmark",
    {%- endif %}
]
source_suffix = [
    ".{{ cookiecutter.__doc_ext }}",
]
master_doc = "index"
version = "{{ cookiecutter.version }}"
release = "{{ cookiecutter.version }}"
autodoc_typehints = "description"
pygments_style = "sphinx"
todo_include_todos = False
{%- if cookiecutter.__use_markdown == "True" %}
# Prefix document path to section labels, otherwise autogenerated labels would look like 'heading'
# rather than 'path/to/file:heading'
autosectionlabel_prefix_document = True
{%- endif %}


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"
{%- if cookiecutter.__use_markdown == "True" %}


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'recommonmark', u'Recommonmark Documentation',
     [author], 1)
]
{%- endif %}


# -- Options for Texinfo output -------------------------------------------

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
        "{{ cookiecutter.project_description }}",
        "Miscellaneous",
    ),
]


# -- Options for Napoleon extension ---------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
{%- if cookiecutter.__use_markdown == "True" %}


# -- App setup hook -------------------------------------------------------

def setup(app):
    app.add_config_value('recommonmark_config', {
        #'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_math': True,
        'enable_inline_math': True,
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)
{%- endif %}
