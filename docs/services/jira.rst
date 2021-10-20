.. _service_jira:

JIRA
====

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

   .. needservice:: jira
       :query: summary !~ "FooBar"
       :prefix: MY_IMPORT_

.. contents:: Page content
   :local:

Options
-------
The following options can be used inside ``.. needservice:: Jira`` and related directives.

query
~~~~~
A query string, which must be valid to `JQL <https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/>`_.

prefix
~~~~~~
A string, which is taken as prefix for the need-id. E.g. ``CB_IMPORT_`` --> ``CB_IMPORT_005``.

Config
------
Most configuration needs to be done via the service configuration in your ``conf.py`` file.

.. hint::

   For details about most configuration options, please take a look into the
   :ref:`common configuration description <service_config>`.

The following documentation describes service specific information for ``Jira`` only.

endpoint
~~~~~~~~
**Default**: ``/rest/api/2/search``

See also :ref:`conf_endpoint` for more details.

query
~~~~~
String, which must follow the `JQL <https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/>`_.
notation.

See also :ref:`conf_query` for more details.


id_prefix
~~~~~~~~~
A prefix for the final ID of the created need.
Can get important, if the IDs from Jira are not unique.

Example: ``JIRA_`` will create IDs like ``JIRA_TEST-3``.

convert_content
~~~~~~~~~~~~~~~
If True, the format used by JIRA for descriptions gets transformed to rst.
This allows Sphinx to render the content.

Otherwise the default format is kept and printed, which would contain also the style
specific information like ``h3.`` for titles.

Drawback: The used converter libraries are quite slow and it will take 1-3 seconds per issue.

**Default**: True

Example
-------
**conf.py**

.. code-block:: python

    needs_services = {
        'jira': {
            'url': "http://127.0.0.1:8081",
            'user': 'test',
            'password': 'test',
            'id_prefix': "JIRA_",
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
        }
    }

**Any rst file**

.. code-block:: rst

   .. needservice:: jira
       :query: project = PX
       :prefix: JIRA_IMPORT

   .. needtable::
      :filter: "JIRA_IMPORT" in id

**Result**

{% if on_ci != true %}

.. needservice:: jira
   :query: project = PX
   :prefix: JIRA_IMPORT

.. needtable::
   :filter: "JIRA_IMPORT" in id

{% else %}
.. hint::

   The below examples are just images, as no Jira instance was available during documentation build.

.. image:: /_images/jira_example.png
   :align: center
   :width: 80%

.. image:: /_images/jira_table.png
   :align: center
   :width: 80%

{% endif %}
