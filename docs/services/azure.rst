.. _service_azure:

Azure
=====

.. contents::
   :local:

The ``Jira`` service synchronizes
data between `Jira <https://www.atlassian.com/software/jira>`_ from `Atlassian <https://www.atlassian.com>`_ and the
life cycle management extension `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ from
`useblocks <https://useblocks.com>`_.

The implementation is based on the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__.

The ``Jira`` service allows to retrieve external data during documentation build and
to create Sphinx-Needs objects based on this data.
After the created Sphinx-Needs objects support every function from
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__, which includes Filtering, Linking,
Updating and much more.

**Example**:

Inside any ``rst`` file of your Sphinx project:

.. code-block:: rst

   .. needservice:: azure
       :query: [System.WorkItemType] = 'Issue'
       :prefix: AZURE_IMPORT_

   .. needtable::
       :filter: "AZURE_IMPORT" in id
       :columns: id, title, status, type
       :style: table



.. needservice:: azure
   :query: [System.WorkItemType] = 'Issue'
   :prefix: AZURE_IMPORT_

.. needtable::
   :filter: "AZURE_IMPORT" in id
   :columns: id, title, status, type
   :style: table
