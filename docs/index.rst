.. Sphinx-Needs Enterprise documentation master file, created by
   sphinx-quickstart on Tue Sep 21 09:02:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: /_static/sphinx-needs-enterprise-logo.png
   :align: center
   :scale: 25%

Welcome
=======

This package provides enterprise specific solutions for ``Sphinx-Needs``.

Its main goal is to embed ``Sphinx-Needs`` in company specific tool environments by
synchronizing data between ``Sphinx-Needs`` and tools like Jira, Azure, GitHub, CodeBeamer and more.

``Sphinx-Needs Enterprise`` features are supporting the following services and tools:


.. grid:: 4
   :gutter: 1

   .. grid-item-card::
      :columns: 12 6 3 3
      :class-card: border

      .. image:: /_static/azuredevops-logo.png
         :align: center
         :target: https://azure.microsoft.com/en-us/services/devops/

      ^^^^^^^^

      :bdg-danger:`BETA`

      .. button-ref:: service_azure
         :color: primary
         :align: left
         :class: service-btn

         needservice

      .. button-ref:: sne_import
         :color: secondary
         :align: left
         :class: service-btn

         sne import

   .. grid-item-card::
      :columns: 12 6 3 3
      :class-card: border

      .. image:: /_static/codebeamer-logo.png
         :align: center
         :target: https://codebeamer.com

      ^^^^^^^^

      :bdg-danger:`BETA`

      .. button-ref:: service_cb
         :color: primary
         :align: left
         :class: service-btn

         needservice

      .. button-ref:: sne_import
         :color: secondary
         :align: left
         :class: service-btn

         sne import

   .. grid-item-card::
      :columns: 12 6 3 3
      :class-card: border

      .. image:: /_static/jira-logo.png
         :align: center
         :target: https://www.atlassian.com/software/jira

      ^^^^^^^^

      :bdg-danger:`BETA`

      .. button-ref:: service_jira
         :color: primary
         :align: left
         :class: service-btn

         needservice

      .. button-ref:: sne_import
         :color: secondary
         :align: left
         :class: service-btn

         sne import

   .. grid-item-card::
      :columns: 12 6 3 3
      :class-card: border

      .. image:: /_static/elasticsearch-logo.png
         :align: center
         :target: https://www.elastic.co/elastic-stack/

      ^^^^^^^^

      :bdg-danger:`BETA`

      .. button-ref:: sne_export
         :color: info
         :align: left
         :class: service-btn

         sne export


``Sphinx-Needs Enterprise`` provides directives and scripts to fetch data inside and outside of a Sphinx
project.

.. warning::

   This package is in the Beta phase. Docs, tests and even the code is not complete and may contain bugs.


.. _index_needservice:

Needservice directive
---------------------

Use ``needservice`` to get the external data directly into your documentation.

.. tab-set::

   .. tab-item:: Azure
      :sync: azure-tab

      .. code-block:: rst

         .. needservice:: azure_config
            :query: [System.WorkItemType] = 'Issue'

      Take a look into our :ref:`needservice with Azure <service_azure>` documentation for technical details.

   .. tab-item::  Codebeamer
      :sync: cb-tab

      .. code-block:: rst

         .. needservice:: codebeamer_config
            :query: project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'

      Take a look into our :ref:`needservice with Codebeamer <service_cb>` documentation for technical details.

   .. tab-item::  Jira
      :sync: jira-tab

      .. code-block:: rst

         .. needservice:: jira_config
            :query: project = my_project

      Take a look into our :ref:`needservice with Jira <service_jira>` documentation for technical details.


SNE script
----------

The ``sne`` script provides solutions for different tasks like getting and storing external data or rendering templates.

Use ``sne import`` as command in your terminal to store external data in JSON files for later manipulation
or for imports into your Sphinx project.

.. tab-set::

   .. tab-item::  Azure
      :sync: azure-tab

      .. code-block:: bash

         sne import azure_config --query "[System.WorkItemType] = 'Issue'"

   .. tab-item::  Codebeamer
      :sync: cb-tab

      .. code-block:: bash

         sne import codebeamer_config --query "project.name IN ('my_project', 'another_project')"

   .. tab-item::  Jira
      :sync: jira-tab

      .. code-block:: bash

         sne import jira_config --query "project = my_project"

After this you can use ``sne render`` to create files, e.g. rst-files, for your Sphinx project based on your templates.

.. code-block:: bash

   sne render -j needs.json -t my_template.rst -o output.rst


See our docs about the :ref:`sne` for more details.

Service configuration
---------------------

Service names like ``jira_config`` are referencing a detailed configuration inside the
``conf.py`` file of a Sphinx project.

This configuration is shared by ``needservice`` and the ``sne`` script.

.. tab-set::

   .. tab-item::  Azure
      :sync: azure-tab

      .. literalinclude:: /snippets/azure_config.py
         :language: python

      For technical details, please read the pages :ref:`needservice with Azure <service_azure>`
      and :ref:`Common service configuration <service_config>`.

   .. tab-item::  Codebeamer
      :sync: cb-tab

      .. literalinclude:: /snippets/cb_config.py
         :language: python

      For technical details, please read the pages :ref:`needservice with Codebeamer <service_cb>`
      and :ref:`Common service configuration <service_config>`.

   .. tab-item::  Jira
      :sync: jira-tab

      .. literalinclude:: /snippets/jira_config.py
         :language: python

      For technical details, please read the pages :ref:`needservice with Jira <service_jira>`
      and :ref:`Common service configuration <service_config>`.


License
-------

``Sphinx-Needs Enterprise`` is **free to use for private projects**.

**Commercial projects must obtain a commercial license**, which guarantees an ongoing and professional development of
``Sphinx-Needs`` and related extensions. For details please see :ref:`license`.


Sphinx-Needs Ecosystem
----------------------

In the last years, we have created additional information and extensions, which are based on or related to Sphinx-Needs:

.. grid:: 2
   :gutter: 2

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://sphinx-needs.com
      :img-top: /_static/sphinx-needs-card.png
      :class-card: border

      Sphinx-Needs.com
      ^^^^^^^^^^^^^^^^
      The website presents the essential Sphinx-Needs functions and related extensions.

      Also, it is a good entry point to understand the benefits and get an idea about the complete ecosystem of Sphinx-Needs.
      +++

      .. button-link:: https://sphinx-needs.com
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`globe;1em;sd-text-primary` Sphinx-Needs.com

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://sphinx-needs.readthedocs.io/en/latest/
      :img-top: /_static/sphinx-needs-card.png
      :class-card: border

      Sphinx-Needs
      ^^^^^^^^^^^^
      Create, update, link, filter and present need objects like Requirements, Specifications, Bugs and many more.

      The base extension provides all of its functionality under the MIT license for free.
      +++

      .. button-link:: https://sphinx-needs.readthedocs.io/en/latest/
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`book;1em;sd-text-primary` Technical Docs

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://useblocks.com/sphinx-needs-enterprise/
      :img-top: /_static/sphinx-needs-enterprise-card.png
      :class-card: border

      Sphinx-Needs Enterprise
      ^^^^^^^^^^^^^^^^^^^^^^^
      Synchronize Sphinx-Needs data with external, company internal systems like CodeBeamer, Jira or Azure Boards.

      Provides scripts to baseline data and makes CI usage easier.
      +++

      .. button-link:: http://useblocks.com/sphinx-needs-enterprise/
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`book;1em;sd-text-primary` Technical Docs

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://sphinx-test-reports.readthedocs.io/en/latest/
      :img-top: /_static/sphinx-test-reports-logo.png
      :class-card: border

      Sphinx-Test-Reports
      ^^^^^^^^^^^^^^^^^^^
      Extension to import test results from XML files as **need** objects.

      Created **need** objects can be filtered and linked to specification objects.
      +++

      .. button-link:: https://sphinx-test-reports.readthedocs.io/en/latest/
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`book;1em;sd-text-primary` Technical Docs


Other Sphinx extensions
~~~~~~~~~~~~~~~~~~~~~~~
During the use of Sphinx-Needs in popular companies’ internal projects,
we have created other Sphinx extensions to support the work of teams in the automotive industry:

.. grid:: 2
   :gutter: 2

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://sphinx-collections.readthedocs.io/en/latest/
      :img-top: /_static/sphinx_collections_logo.png
      :class-card: border

      Sphinx Collections
      ^^^^^^^^^^^^^^^^^^
      Extension to collect or generate files from different sources and include them in the Sphinx source folder.

      It supports sources like Git repositories, Jinja based files or symlinks.
      +++

      .. button-link:: https://sphinx-collections.readthedocs.io/en/latest/
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`book;1em;sd-text-primary` Technical Docs

   .. grid-item-card::
      :columns: 12 6 6 6
      :link: https://sphinx-bazel.readthedocs.io/en/latest/
      :img-top: /_static/sphinx_bazel_logo.png
      :class-card: border

      Sphinx Bazel
      ^^^^^^^^^^^^
      Provides a Bazel domain in Sphinx documentation and allows the automated import of Bazel files and their documentation.
      +++

      .. button-link:: https://sphinx-bazel.readthedocs.io/en/latest/
         :color: primary
         :outline:
         :align: center
         :expand:

         :octicon:`book;1em;sd-text-primary` Technical Docs


.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   scripts/index
   services/index
   api/index
   contribute
   license
   changelog


