.. Sphinx-Needs Enterprise documentation master file, created by
   sphinx-quickstart on Tue Sep 21 09:02:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: /_static/sphinx-needs-enterprise-logo.png
   :align: center
   :scale: 35%

Welcome
=======

This package provides enterprise specific solutions for ``Sphinx-Needs``.

Its main goal is to embed ``Sphinx-Needs`` in company specific tool environments by
synchronizing data between ``Sphinx-Needs`` and tools like Jira, Doors, GitHub, CodeBeamer and more.

``Sphinx-Needs Enterprise`` provides directives and scripts to fetch data inside and outside of a Sphinx
project.

Inside a rst-file:

.. code-block:: rst

   .. needservice:: jira_config
      :query: project = my_project

As script to store data inside a ``needs.json`` file:

.. code-block:: bash

   sne import jira_config --query "project = my_project"

Supported tools:

* **CodeBeamer**
* **Jira**

Support for following tools is planned: Doors, GitHub Enterprise, Azure Boards

.. warning::

   This package is in an early Alpha phase. Docs, tests and even the code is not complete and may contain bugs.

   So do not use it for production.

License
-------
``Sphinx-Needs Enterprise`` is **free to use for private projects**.

**Commercial projects must obtain a commercial license**, which guarantees an ongoing and professional development of
``Sphinx-Needs`` and related extensions. For details please see :ref:`license`.


Content
-------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   scripts/index
   services/index
   api/index
   contribute
   license
   changelog


