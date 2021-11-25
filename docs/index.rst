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
synchronizing data between ``Sphinx-Needs`` and tools like Jira, Doors, GitHub, CodeBeamer and more.

``Sphinx-Needs Enterprise`` features are supporting the following services and tools:

.. panels::
   :container: container-lg pb-3
   :column: col-lg-3 col-md-3 col-sm-6 col-xs-6 p-2

   .. image:: /_static/azuredevops-logo.png
      :align: center
      :height: 100px
      :target: https://azure.microsoft.com/en-us/services/devops/

   :badge:`BETA, badge-danger`
   :link-badge:`service_azure,needservice,ref, badge-primary text-white`
   :link-badge:`sne_import,sne import,ref,badge-secondary text-white`
   ---
   .. image:: /_static/codebeamer-logo.png
      :align: center
      :height: 100px
      :target: https://codebeamer.com

   :badge:`BETA, badge-danger`
   :link-badge:`service_cb,needservice,ref, badge-primary text-white`
   :link-badge:`sne_import,sne import,ref,badge-secondary text-white`
   ---
   .. image:: /_static/jira-logo.png
      :align: center
      :height: 100px
      :target: https://www.atlassian.com/software/jira

   :badge:`BETA, badge-danger`
   :link-badge:`service_jira,needservice,ref, badge-primary text-white`
   :link-badge:`sne_import,sne import,ref,badge-secondary text-white`
   ---
   .. image:: /_static/elasticsearch-logo.svg
      :align: center
      :height: 100px
      :target: https://www.elastic.co/elastic-stack/

   :badge:`BETA, badge-danger`
   :link-badge:`sne_export,sne export,ref,badge-info`

``Sphinx-Needs Enterprise`` provides directives and scripts to fetch data inside and outside of a Sphinx
project.

.. warning::

   This package is in an Beta phase. Docs, tests and even the code is not complete and may contain bugs.


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


Sphinx-Needs Ecosystem
----------------------
In the last years additional information and extensions have been created, which are based or related to Sphinx-Needs:


.. panels::
   :container: container-lg pb-3
   :column: col-lg-6 col-md-6 col-sm-4 col-xs-4 p-2
   :img-top-cls: pl-5 pr-5 pt-2 pb-2

   ---
   :img-top: /_static/sphinx-needs-card.png
   :img-top-cls: + bg-light

   Sphinx-Needs.com
   ^^^^^^^^^^^^^^^^
   Webpage to present most important Sphinx-Needs functions and related extensions.

   Good entrypoint to understand the benefits and to get an idea about the complete ecosystem of Sphinx-Needs.

   +++

   .. link-button:: https://sphinx-needs.com
       :type: url
       :text: Sphinx-Needs.com
       :classes: btn-secondary btn-block

   ---
   :img-top: /_static/sphinx-needs-card.png

   Sphinx-Needs
   ^^^^^^^^^^^^
   Base extension, which provides all of its functionality under the MIT license for free.

   Create, update, link, filter and present need objects like Requirements, Specifications, Bugs and much more.

   +++

   .. link-button:: https://sphinxcontrib-needs.readthedocs.io/en/latest/
       :type: url
       :text: Technical docs
       :classes: btn-secondary btn-block

   ---
   :img-top: /_static/sphinx-needs-enterprise-card.png

   Sphinx-Needs Enterprise
   ^^^^^^^^^^^^^^^^^^^^^^^
   Synchronizes Sphinx-Needs data with external, company internal systems like CodeBeamer, Jira or Azure Boards.

   Provides scripts to baseline data and make CI usage easier.
   +++

   .. link-button:: http://useblocks.com/sphinx-needs-enterprise/
       :type: url
       :text: Technical docs
       :classes: btn-secondary btn-block

   ---
   :img-top: /_static/sphinx-test-reports-logo.png

   Sphinx-Test-Reports
   ^^^^^^^^^^^^^^^^^^^
   Extension to import test results from xml files as need objects.

   Created need objects can be filtered and e.g. linked to specification objects.
   +++

   .. link-button:: https://sphinx-test-reports.readthedocs.io/en/latest/
       :type: url
       :text: Technical docs
       :classes: btn-secondary btn-block


Further Sphinx extensions
^^^^^^^^^^^^^^^^^^^^^^^^^
During the work with Sphinx-Needs in bigger, company internal projects, other Sphinx extensions have been created
to support the work in teams of the automotive industry:

.. panels::
   :container: container-lg pb-3
   :column: col-lg-6 col-md-6 col-sm-4 col-xs-4 p-2
   :img-top-cls: pl-5 pr-5 pt-2 pb-2

   ---
   :img-top: /_static/sphinx_collections_logo.png


   Extension to collect or generate files from different sources and include them into the Sphinx source folder.

   Sources like git repositories, jinja based files or symlinks are supported.

   +++

   .. link-button:: https://sphinx-collections.readthedocs.io/en/latest/
       :type: url
       :text: Technical docs
       :classes: btn-secondary btn-block

   ---
   :img-top: /_static/sphinx_bazel_logo.png


   Provides a Bazel domain in Sphinx documentations and allows the automated import of Bazel files and their
   documentation.

   +++

   .. link-button:: https://sphinx-bazel.readthedocs.io/en/latest/
       :type: url
       :text: Technical docs
       :classes: btn-secondary btn-block

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


