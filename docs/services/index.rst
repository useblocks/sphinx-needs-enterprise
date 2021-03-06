Services
========
Services are used to get objects like Issues from external services like JIRA and create Sphinx-Needs objects based
on them.

Write ``.. needservice:: <service>`` into any rst-file and the related service will add the received data
as Sphinx-Needs objects.

``Sphinx-Needs Enterprise`` supports the following services:

.. toctree::
   :maxdepth: 2

   azure
   codebeamer
   jira
   excel

.. _service_config:

Configuration
-------------
Most services share a common set of configuration parameters, which are described on this page.

.. contents::
   :local:

{% raw %}

.. code-block:: python

    my_content = """
    **Raw description of content**

    {{data.description}}
    """

    needs_services = {
        'my_service': {
            'url': "http://127.0.0.1:8081",
            'endpoint': "/custom/rest/endpoint"
            'user': 'test',
            'password': 'test',
            'id_prefix': "SERVICE_",
            'query': 'project = TEST',
            'content': my_content,
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
            'raw': 'False',
            'wiki2html: 'True',
        }
    }

{% endraw %}

.. _conf_url:

url
~~~
``URL`` of the server. The final ``REST`` api location gets added automatically.

.. _conf_endpoint:

endpoint
~~~~~~~~
The final address of the ``endpoint``.

Is service specific, but the configured default values should work for most cases.

.. _conf_credentials:

user/password
~~~~~~~~~~~~~
Credentials used for login.

.. _conf_query:

query
~~~~~
A string which represents the query parameter. The syntax of the query string is service specific.

It can be overwritten by option ``query`` of the ``needservice`` directive.

.. code-block:: rst

   .. needservice:: JIRA
      :query: status not in ('Closed', 'Resolved', 'Done')

See related service description for details.

.. _conf_id_prefix:

id_prefix
~~~~~~~~~
A prefix for the final ID of the created need.
Can get important, if the IDs from Codebeamer are not unique.

Example: ``CB_`` will create IDs like ``CB_1002``.

.. _conf_mapping:

mapping
~~~~~~~
{% raw %}

The field names of a service object do not often map to option names of Sphinx-Needs.
So **mapping** defines where a Sphinx-Needs option shall get its value inside the service data.

**mapping** must be a dictionary, where the **key** is the needs object name and the **value** is either
a Jinja string such as ``is_{{status}}`` or a list/tuple, which defines the location of the value in the retrieved
service data object.

**Example using a Jinja string as value for the Excel service**

Goal: The need option ``author`` shall be set to both the Last and First names.

The last and first names information are stored in the retrieved Excel data under ``LAST_NAME`` and ``FIRST_NAME``.

.. image:: /_images/excel_data.png
   :align: center
   :width: 80%

So the final ``mapping`` entry looks like:

.. code-block:: python

    'mapping': {
        'author': "{{LAST_NAME}} {{FIRST_NAME}}",
    }


.. note::
   When you use a Jinja string as value, you must ensure the field names of a service object,
   set as values for the mapping option, does not contain spaces because that will raise a
   `Jinja Template Syntax Error <https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError>`_.
   For example: Instead of the column name being ``CREATED AT`` use ``CREATED_AT``. Read more about the :ref:`conf_mapping`
   configuration.

{% endraw %}

**Example using a list/tuple as value for the Codebeamer service**

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

.. note::

   Combining data from multiple locations in a mapping definition is currently not supported.

.. _conf_mappings_replaces:

mappings_replaces
~~~~~~~~~~~~~~~~~
There are use cases, where a value inside service data is not valid for a Sphinx-Needs options.

For instance: In Codebeamer the type is named ``Requirement``, but Sphinx-Needs supports only ``req`` as value
for ``type`` option.

``mappings_replaces`` can replace strings defined by a regular expression with a new value.
This replacement is performed for **all** mappings.

**Example**

The Codebeamer value ``Requirement`` must be replaced by ``req`` and set as value for the need option ``type``.

.. code-block:: python

    'codebeamer': {
        'mappings': {
            'type': ['typeName'],  # maps the original location
        },
        'mappings_replaces': {
            '^Requirement$': 'req',
        }
    }

.. _conf_content:

content
~~~~~~~
{% raw %}
``content`` takes a string, which gets interpreted as rst-code for the need-content area.
Jinja support is also available, so that service data is available and can be accessed like
``{{data.description}}``.

Example for a Codebeamer configuration:

.. code-block:: python

    my_content = """
    Content from Codebeamer Issue
    -----------------------------
    ``{{data.description}}``.

    This is assigned to **{{data.assignedTo[0].name]}}**.

    `Link to source <http://my_server/issue/{{data.id}}>`_
    """

    needs_services = {
    'codebeamer': {
        # ... some other values
        'content': my_content
        }
    }

The set options for the ``needservice`` are available  under ``options``. Example:

.. code-block:: python

   my_content = """
   Executed query: {{options.query}}

   {{data.description}}

   {% if options.prefix == "TEST_" %}
   **TEST TICKET**
   {% endif %}
   """

{% endraw %}

.. _conf_extra_data:

extra_data
~~~~~~~~~~
There may be information stored inside a service's data fields that can not be mapped to Sphinx-Needs options, but
shall be made available inside the needed object.

This can be done by using ``extra_data``, which adds this  kind of information to the end of the content of a
need object.

The logic and syntax are the same as used by :ref:`conf_mapping`.

.. code-block:: python

        'extra_data': {
            'assignedBy': ['assignedTo', 0, 'name'],
            'createdAt': ['createdAt'],
            'updated': ['modifiedAt'],
        }

.. _conf_raw:

raw
~~~
Outputs the needed content to a codeblock without any modifications.

For some services a content transformation (e.g. wiki-syntax to HTML or rst) is needed, to get a nice looking and
"working" representation of the content.

Default: False

Supported Services: Codebeamer

.. _conf_wiki2html:

wiki2html
~~~~~~~~~
Transforms a needed content, that uses a wiki-like syntax, to a format Sphinx can use (e.g
rst or HTML).

Most services do not need to support these configuration options, as they provide by default a Sphinx compatible
output.

Default: True

Supported Services: Codebeamer
