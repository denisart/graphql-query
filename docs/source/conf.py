# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'graphql_query'
copyright = '2022-2023, Denis A. Artyushin'
author = 'Denis A. Artyushin'
version = '1.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinxarg.ext',
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# -- AutoDoc configuration -------------------------------------------------
# autoclass_content = "both"

autodoc_default_options = {
    'members': True,
    'inherited-members': False,
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}

autosummary_generate = True
