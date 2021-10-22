# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime

from docutils.parsers.rst import directives

sys.path.insert(0, os.path.abspath('../sphinx_needs_enterprise'))


# -- Project information -----------------------------------------------------

project = 'Sphinx-Needs Enterprise'
now = datetime.datetime.now()
copyright = '{year}, useblocks.com'.format(year=now.year)
author = 'team useblocks'

# The full version, including alpha/beta/rc tags
release = '1.0'
version = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    'sphinx.ext.intersphinx',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.needs',
    'sphinx_needs_enterprise',
    'sphinx_panels',
    'sphinxcontrib.programoutput'
]

intersphinx_mapping = {'needs': ('https://sphinxcontrib-needs.readthedocs.io/en/latest/', None)}

cb_server = 'http://127.0.0.1:8080'

azure_content = """
Item URL: `{{fields["System.TeamProject"]}}/{{id}} <https://dev.azure.com/useblocks/{{fields["System.TeamProject"]}}/_workitems/edit/{{id}}>`_
 
.. raw:: html

   {{fields["System.Description"]}}"""

cb_content = """
`Codebeamer Link to Issue {{id}} <{cb_server}/issue/{{id}}>`_

{{description}}"""

jira_content = """
{{fields.description}}"""

needs_services = {
    'azure_config': {
        'url': os.getenv('NEEDS_AZURE_URL', 'https://dev.azure.com/useblocks'),
        'token': os.getenv('NEEDS_AZURE_TOKEN', ''),
        'id_prefix': "AZURE_",
        'query':  "[System.WorkItemType] = 'Issue'",
        'content': azure_content,
        'mappings': {
            "id": ["id"],
            "type": 'spec',
            "title": ["fields", "System.Title"],
            "status": ["fields", "System.State"],
        },
        'extra_data': {
            "Original Type": ["fields", 'System.WorkItemType'],
            "Original Assignee": ["fields", 'System.AssignedTo', 'displayName'],
        }
    },
    'codebeamer_config': {
        'license_key': 'IRKTJ-RVCQS-KSNCP-ZHYBA',
        'url': "http://127.0.0.1:8080",
        'user': 'bond',
        'password': '007',
        'prefix': "CB_IMPORT_",
        'content': cb_content,
        'query': "project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'",
        'mappings': {
            'type': "spec",
            'tags': 'cb_import, example',
            "id": ["id"],
            "status": ["status", "name"],
            "title": ["name"],
        },
        'extra_data': {
            'assignedBy': ['assignedTo', 0, 'name'],
            'createdAt': ['createdAt'],
            'updated': ['modifiedAt'],
            'type': ['typeName'],
        }
    },
    'jira_config': {
        'license_key': 'IRKTJ-RVCQS-KSNCP-ZHYBA',
        'url': "http://127.0.0.1:8081",
        'user': 'test',
        'password': 'test',
        'id_prefix': "JIRA_",
        'query': "project = PX",
        'mappings': {
            "id": ["key"],
            "type": 'spec',
            "title": ["fields", "summary"],
            "status": ["fields", "status", "name"],
        },
        'extra_data': {
            "Original Type": ["fields", "issuetype", "name"],
            "Original Assignee": ["fields", "assignee", "displayName"],
        }
    },
    'test': {},
}

needs_extra_options = ["author"]

needs_types = [dict(directive="req", title="Requirement", prefix="R_", color="#BFD8D2", style="node"),
               dict(directive="spec", title="Specification", prefix="S_", color="#FEDCD2", style="node"),
               dict(directive="impl", title="Implementation", prefix="I_", color="#DF744A", style="node"),
               dict(directive="test", title="Test Case", prefix="T_", color="#DCB239", style="node"),
               dict(directive="task", title="Task", prefix="T_", color="#DCB239", style="node"),
               # Kept for backwards compatibility
               dict(directive="need", title="Need", prefix="N_", color="#9856a5", style="node")
           ]


def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    # Make sure we're outputting HTML
    if app.builder.format != 'html':
        return
    src = source[0]
    rendered = app.builder.templates.render_string(
        src, app.config.html_context
    )
    source[0] = rendered


# Check, if docs get buil on ci.
# If this is the case, external services like Codebeamer are not available and
# docs will show images instead of gettting real data.
on_ci = os.environ.get('ON_CI', 'False').upper() == 'TRUE'


def setup(app):
    print(f'---> ON_CI is: {on_ci}')
    app.connect("source-read", rstjinja)


html_context = {
    'on_ci': on_ci
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = os.environ.get('THEME', 'sphinx_material')


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Set link name generated in the top bar.
html_title = 'Sphinx-Needs Enterprise'

# Material theme options (see theme.conf for more information)
html_theme_options = {
    'table_classes': [''],

    # Set the name of the project to appear in the navigation.
    'nav_title': 'Sphinx-Needs Enterprise',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://project.github.io/project',

    # Set the color and the accent color
    'theme_color': '#2a639a',
    'color_primary': '#2a639a',
    'color_accent': '#2a639a',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/useblocks/sphinx-needs-enterprise/',
    'repo_name': '',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 2,
    # If False, expand all TOC entries
    'globaltoc_collapse': True,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
    "nav_links": [
        {
            "href": "https://sphinx-needs.com",
            "internal": False,
            "title": "Sphinx-Needs",
        },
        {
            "href": "https://sphinxcontrib-needs.readthedocs.io/en/latest/",
            "internal": False,
            "title": "Sphinx-Needs Docs",
        },
    ],
    "heroes": {
        "index": "Enterprise Solutions for Sphinx-Needs",
        "services/index": "Synchronize with external services",
    },
}
panels_css_variables = {
    "tabs-color-label-active": "rgb(42, 99, 154)",
    "tabs-color-label-inactive": "rgb(42, 99, 154, 0.6)",
    "tabs-color-overline": "rgb(42, 99, 154)",
    "tabs-color-underline": "rgb(42, 99, 154)",
    "tabs-size-label": "0.9rem",
}

html_css_files = [
    'custom.css'
]

if html_theme == "sphinx_material":
    html_sidebars = {
        "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
    }

