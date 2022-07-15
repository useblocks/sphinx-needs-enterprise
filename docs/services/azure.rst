.. _service_azure:

Azure
=====
The ``Azure`` service synchronizes
data between `Azure DevOps Boards/WorkItems <https://azure.microsoft.com/en-us/services/devops/boards/>`_ and the
life cycle management extension `Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/latest/>`_ from
`useblocks <https://useblocks.com>`_.

The implementation is based on the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/latest/>`__.

The ``Azure`` service allows to retrieve external data during documentation build and
to create Sphinx-Needs objects based on this data.
After the created Sphinx-Needs objects support every function from
`Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/latest/>`__, which includes Filtering, Linking,
Updating and much more.

Options
-------
The following options can be used inside ``.. needservice:: Azure`` and related directives.

query
~~~~~
A query string, which must be valid to
`WIQL <https://docs.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops>`_.

prefix
~~~~~~
A string, which is taken as prefix for the need-id. E.g. ``AZURE_IMPORT`` --> ``AZURE_IMPORT_001``.

Config
------
An Azure service configuration must be created inside your ``conf.py`` file.

.. hint::

   For details about most configuration options, please take a look into the
   :ref:`common configuration description <service_config>`.

The following documentation describes service specific information for ``Azure`` only.

url
~~~
The ``url`` should look like``https://dev.azure.com/<company>"``, where ``<company>`` must be replaced.

Please see :ref:`conf_url` for more details.

token
~~~~~
Instead of a ``user`` and a ``password``, Azure DevOps need a personal access token.

Which can be created under ``https://dev.azure.com/<company>/_usersSettings/tokens``.

Example
-------
Inside your ``conf.py`` file:

.. literalinclude:: /snippets/azure_config.py
      :language: python

Inside any ``rst`` file of your Sphinx project:

.. code-block:: rst

   .. needservice:: azure_config
       :query: [System.WorkItemType] = 'Issue'
       :prefix: AZURE_IMPORT_

   .. needtable::
       :filter: "AZURE_IMPORT" in id
       :columns: id, title, status, type
       :style: table

**Result**

.. needservice:: azure_config
   :query: [System.WorkItemType] = 'Issue'
   :prefix: AZURE_IMPORT_

.. needtable::
   :filter: "AZURE_IMPORT" in id
   :columns: id, title, status, type
   :style: table
