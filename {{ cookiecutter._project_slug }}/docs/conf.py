"""Sphinx configuration."""
import recommonmark
from datetime import datetime
from recommonmark.transform import AutoStructify


# -- Project inforrmation -------------------------------------------------

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.author }}"
copyright = f"{datetime.now().year}, {author}"


# -- Base Sphinx configuration --------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
    {% if cookiecutter._use_markdown -%}
    "recommonmark",
    "sphinx.ext.autosectionlabel",
    {%- endif %}
]
source_suffix = [
    ".{{ cookiecutter._doc_ext }}",
]
master_doc = "index"
version = "{{ cookiecutter.version }}"
release = "{{ cookiecutter.version }}"
autodoc_typehints = "description"
pygments_style = "sphinx"
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'recommonmark', u'Recommonmark Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, project, f"{project} Documentation",
     author, project, "{{ cookiecutter.project_description }}",
     "Miscellaneous"),
]


# -- App setup hook -------------------------------------------------------

def setup(app):
    app.add_config_value('recommonmark_config', {
        #'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_math': False,
        'enable_inline_math': True,
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)
