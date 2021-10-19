.. _service_cb:

Codebeamer
==========

.. contents::
   :local:

The ``Codebeamer`` service synchronizes
data between `codebeamer <https://codebeamer.com/>`_ from `Intland <https://intland.com/>`_ and the
Requirement Engineering extension `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ from
`useblocks <https://useblocks.com>`_.

The implementation is based on the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__.

The ``Codebeamer`` service allows to retrieve external data during documentation build and
to create Sphinx-Needs objects based on this data.
After the created Sphinx-Needs objects support every function from
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__, which includes Filtering, Linking,
Updating and much more.

**Example**:

Inside any ``rst`` file of your Sphinx project:

.. code-block:: rst

   .. needservice:: codebeamer
       :query: project.name IN ('my_project', 'another_project')
       :prefix: MY_IMPORT_

.. contents:: Page content
   :local:

Options
-------
:query: A query string, which must be valid to `cbQL <https://codebeamer.com/cb/wiki/871101>`_.
:prefix: A string, which is taken as prefix for the need-id. E.g. ``CB_IMPORT_`` --> ``CB_IMPORT_005``.

Config
------
A codebeamer service configuration must be created inside your ``conf.py`` file.

.. hint::

   For details about most configuration options, please take a look into the
   :ref:`common configuration description <service_config>`.

The following documentation describes service specific information for ``Codebeamer`` only.

endpoint
~~~~~~~~
Default value for ``Codebeamer`` services is ``/rest/v3/items/query``.

See also :ref:`conf_endpoint` for more details.

url
~~~
Please see :ref:`conf_url` for details.

For Codebeamer REST call this specific location is used: ``/rest/v3/items/query``.

Example
-------
**conf.py**

.. code-block:: python

    needs_services = {
        'codebeamer': {
            'url': "http://127.0.0.1:8080",
            'user': 'bond',
            'password': '007',
            'prefix': "CB_IMPORT_",
            'mapping': {
                'id': ['id'],
                'type': ['typeName'],
                'status': ['status', 'name'],
                'title': ['name'],
                'author': ['createdBy', 'name'],
            },
            'mapping_replaces': {
                '^Task$': 'task',
                '^Requirement$': 'req',
                '^Specification$': 'spec',
            },
            'extra_data': {
                'assignedBy': ['assignedTo', 0, 'name'],
                'createdAt': ['createdAt'],
                'updated': ['modifiedAt'],
            }
        }
    }

**Any rst file**

.. code-block:: rst

   .. needservice:: codebeamer
       :query: project.name IN ('my_project', 'another_project')
       :prefix: CB_IMPORT

   .. needtable::
      :filter: "CB_IMPORT" in id

**Result**

{% if on_ci != true %}

.. needservice:: codebeamer
   :query: project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'
   :prefix: CB_IMPORT_

.. needtable::
   :filter: "CB_IMPORT" in id

{% else %}
.. hint::

   The below examples are just images, as no Codebeamer instance was available during documentation build.

.. image:: /_images/cb_example.png
   :align: center
   :width: 60%

.. image:: /_images/cb_table.png
   :align: center
   :width: 60%

{% endif %}



