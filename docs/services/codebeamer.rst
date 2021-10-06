.. _service_cb:

Codebeamer
==========

.. contents::
   :local:

The ``Codebeamer`` service synchronizes
data between `codebeamer <https://codebeamer.com/>`_ from `Intland <https://intland.com/>`_ and the
Requirement Engineering extension `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ from
`useblocks <https://useblocks.com>`_.

``Sphinx-Needs-Codebeamer`` uses the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__.

This allows to retrieve external data during documentation build and create Sphinx-Needs objects based on this data.
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
{% raw %}
You must also create a codebeamer service configuration in your ``conf.py`` file.

.. code-block:: python

   my_content =  """
   Issues content:

   {{description}}
   """

   needs_services = {
        'codebeamer': {
            'url': 'https://my_codebeamer.com',
            'id_prefix': 'CB_',
            'mapping': {
                'type': ['typeName'],
                'id': ['id'],
                'title': ['name'],
            },
            'mapping_replaces': {
                '^Task$': 'task',
                '^Requirement$': 'req',
                '^Specification$': 'spec',
            },
            'content': my_content,
            'extra_data': {
                'assignedBy': ['assignedTo', 0, 'name'],
                'createdAt': ['createdAt'],
            }
        }
    }
{% rawend %}

url
~~~
``URL`` of the server. The final ``REST`` api location gets added automatically. which is by default
``/rest/v3/items/query``.

id_prefix
~~~~~~~~~
A prefix for the final ID of the created need.
Can get important, if the IDs from Codebeamer are not unique.

Example: ``CB_`` will create IDs like ``CB_1002``.

.. _mapping:

mapping
~~~~~~~
Field names from Codebeamer do normally not map to option names of Sphinx-Needs.
So ``mapping`` defines, from where a Sphinx-Needs option shall get its value inside the Codebeamer data.

``mapping`` must be a dictionary, where the **key** is the needs object name and the **value** is a list or tuple,
which defines the location of the value in the retrieved Codebeamer data object.

**Example**

Goal: The need option ``author`` shall be set to the Assignee name.

This information is stored in the retrieved Codebeamer json data under ``assignedTo.0.name``.

.. image:: /_images/cb_json.png
   :align: center
   :width: 80%

So the final ``mapping`` entry looks like:

.. code-block:: python

    'mapping': {
        'author': ['assignedTo', 0, 'name'],
    }

**Note**: Mapping data from multiple locations, e.g. because ``asssignedTo`` contains is list,
is currently not supported.

mapping_replaces
~~~~~~~~~~~~~~~~
There are use cases, where a value inside Codebeamer data is not valid for a Sphinx-Needs options.

For instance: In Codebeamer the type is named ``Requirement``, but Sphinx-Needs supports only ``req`` as value
for ``type`` option.

``mappings_replaces`` can replace strings defined by a regular expression with a new value.
This replacement is performed for **all** mappings.

**Example**

The Codebeamer value ``Requirement`` must be replaced by ``req`` and set as value for the need option ``type``.

.. code-block:: python

    'codebeamer': {
        'mapping': {
            'type': ['typeName'],  # maps the original location
        },
        'mapping_replaces': {
            '^Requirement$': 'req',
        }
    }

content
~~~~~~~
{% raw %}
``content`` takes a string, which gets interpreted as rst-code for the need-content area.
Jinja support is also available, so that data retrieved from Codebeamer is available and can be accessed like
``{{description}}``.

Example:

.. code-block:: python

    needs_services = {
        'content': """
    Content from Codebeamer Issue
    -----------------------------
    ``{{description}}``.

    This is assigned to **{{assignedTo[0].name]}}**``.

    `Link to source <http://my_server/issue/{{id}}>`_
    """
    }
{% endraw %}
extra_data
~~~~~~~~~~
There may be information stored inside Codebeamer fields, which can not be mapped to Sphinx-Needs options, but
which shall be make available inside the need object.

This can be done by using ``extra_data``, which adds this kind of information to the end of the content of a
need object.

The logic and syntax is the same as used by :ref:`mapping`.

.. code-block:: python

        'extra_data': {
            'assignedBy': ['assignedTo', 0, 'name'],
            'createdAt': ['createdAt'],
            'updated': ['modifiedAt'],
        }



Example
-------
**conf.py**

.. code-block:: python

    needs_services = {
        'codebeamer': {
            'url': "http://127.0.0.1:8080",
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

**Result**

blab: {{on_rtd}}

{% if on_rtd!=False %}
Make...

.. needservice:: codebeamer
   :query: project.name IN ('my_project', 'another_project')
   :prefix: CB_IMPORT_

{% elif on_rtd==True %}
.. hint::

   The below examples are just images, as no CodeBeamer instance is available on ReadTheDocs to generate this
   data during build phase.

.. image:: /_images/cb_example.png
   :align: center
   :width: 100%

{% endif %}

Filtering
---------

.. code-block:: rst

   .. needtable::
      :filter: "CB_IMPORT" in id

{% if on_rtd!=False %}
.. needtable::
   :filter: "CB_IMPORT" in id
   :style: table

{% elif on_rtd==True %}
.. image:: /_images/cb_table.png
   :align: center
   :width: 100%

{% endif %}
