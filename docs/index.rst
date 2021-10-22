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

``Sphinx-Needs Enterprise`` features are supporting the following services and tools:

.. panels::
   :container: container-lg pb-3
   :column: col-lg-4 col-md-4 col-sm-4 col-xs-4 p-2

   .. image:: /_static/azuredevops-logo.png
      :align: center
      :height: 100px
   ---
   .. image:: /_static/codebeamer-logo.png
      :align: center
      :height: 100px
   ---
   .. image:: /_static/jira-logo.png
      :align: center
      :height: 100px

``Sphinx-Needs Enterprise`` provides directives and scripts to fetch data inside and outside of a Sphinx
project.

.. warning::

   This package is in an Alpha phase. Docs, tests and even the code is not complete and may contain bugs.


.. _index_needservice:

Needservice directive
---------------------
Use ``needservice`` to get the external data directly into your documentation.

.. tabbed::  Azure

   .. code-block:: rst

      .. needservice:: azure_config
         :query: [System.WorkItemType] = 'Issue'

   Take a look into our :ref:`needservice with Azure <service_azure>` documentation for technical details.

.. tabbed::  Codebeamer

   .. code-block:: rst

      .. needservice:: codebeamer_config
         :query: project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'

   Take a look into our :ref:`needservice with Codebeamer <service_cb>` documentation for technical details.

.. tabbed::  Jira

   .. code-block:: rst

      .. needservice:: jira_config
         :query: project = my_project

   Take a look into our :ref:`needservice with Jira <service_jira>` documentation for technical details.


SNE script
----------
The ``sne`` script provides solutions for different tasks like getting and storing external data or rendering templates.

Use ``sne import`` as command in your terminal to store external data in json files for later manipulation
or for imports into your Sphinx project.

.. tabbed::  Azure
   :new-group:

   .. code-block:: bash

      sne import azure_config --query "[System.WorkItemType] = 'Issue'"

.. tabbed::  Codebeamer

   .. code-block:: bash

      sne import codebeamer_config --query "project.name IN ('my_project', 'another_project')"

.. tabbed::  Jira

   .. code-block:: bash

      sne import jira_config --query "project = my_project"

After this you can use ``sne render`` to create e.g. rst-files for your Sphinx project based on own templates.

.. code-block:: bash

   sne render -j needs.json -t my_template.rst -o output.rst


See our docs about the :ref:`sne` for more details.

Service configuration
---------------------
Service names like ``jira_config`` are referencing a detailed configuration inside the
``conf.py`` file of a Sphinx project.

This configuration is shared by ``needservice`` and the ``sne`` script.

.. tabbed::  Azure
   :new-group:

   .. literalinclude:: /snippets/azure_config.py
      :language: python

   For technical details, please read the pages :ref:`needservice with Azure <service_azure>`
   and :ref:`Common service configuration <service_config>`.

.. tabbed::  Codebeamer

   .. literalinclude:: /snippets/cb_config.py
      :language: python

   For technical details, please read the pages :ref:`needservice with Codebeamer <service_cb>`
   and :ref:`Common service configuration <service_config>`.

.. tabbed::  Jira

   .. literalinclude:: /snippets/jira_config.py
      :language: python

   For technical details, please read the pages :ref:`needservice with Jira <service_jira>`
   and :ref:`Common service configuration <service_config>`.


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


