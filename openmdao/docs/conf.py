# -*- coding: utf-8 -*-
# This file is execfile()d with the current directory set to its
# containing dir.
import sys
import os
import textwrap
from numpydoc.docscrape import NumpyDocString, Reader
from mock import Mock
from openmdao.docs.config_params import MOCK_MODULES, IGNORE_LIST
from openmdao.docs._utils.patch import do_monkeypatch

sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# start off running the monkeypatch to keep options/parameters
# usable in docstring for autodoc.


def __init__(self, docstring, config={}):
    """
    init
    """
    docstring = textwrap.dedent(docstring).split('\n')

    self._doc = Reader(docstring)
    self._parsed_data = {
        'Signature': '',
        'Summary': [''],
        'Extended Summary': [],
        'Parameters': [],
        'Options': [],
        'Returns': [],
        'Yields': [],
        'Raises': [],
        'Warns': [],
        'Other Parameters': [],
        'Attributes': [],
        'Methods': [],
        'See Also': [],
        'Notes': [],
        'Warnings': [],
        'References': '',
        'Examples': '',
        'index': {}
    }

    try:
        self._parse()
    except ParseError as e:
        e.docstring = orig_docstring
        raise

    # In creation of docs, remove private Attributes (beginning with '_')
    # with a crazy list comprehension
    self._parsed_data["Attributes"][:] = [att for att in self._parsed_data["Attributes"]
                                          if not att[0].startswith('_')]

NumpyDocString.__init__ = __init__

do_monkeypatch()

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('./_exts'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.5'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'numpydoc',
    'show_unittest_examples',
    'embed_code',
    'embed_test',
    'embed_compare',
    'tags'
]

numpydoc_show_class_members = False

# autodoc_default_flags = ['members']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'OpenMDAO'
copyright = u'2016, openmdao.org'
author = u'openmdao.org'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# version = openmdao.__version__
version = "2.0.0"
# The full version, including alpha/beta/rc tags.
# release = openmdao.__version__ + ' Alpha'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None


# exclude_patterns is a list of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
from openmdao.docs._utils.generate_sourcedocs import generate_docs
exclude_patterns = ['_build', '_srcdocs/dev']
absp = os.path.join('.', '_srcdocs')
sys.path.insert(0, os.path.abspath(absp))
generate_docs()

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = '_theme'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['.']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/OpenMDAO_Logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/OpenMDAO_Favicon.ico'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# Output file base name for HTML help builder.
htmlhelp_basename = 'OpenMDAOdoc'

#Customize sidebar
html_sidebars = {
   '**': ['globaltoc.html']
}
# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'openmdao', u'OpenMDAO Documentation',
     [author], 1)
]
