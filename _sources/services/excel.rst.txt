.. _service_excel:

Excel
=====
The ``Excel`` service imports data from spreadsheets to Sphinx-project using Sphinx-Needs and creates Sphinx-Needs objects on the fly during build time.

The implementation is based on the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/latest/>`__.

The ``Excel`` service allows retrieving external data from spreadsheets during documentation build and
creates Sphinx-Needs objects based on this data.
After the creation of the Sphinx-Needs objects, it supports every function from
`Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/latest/>`__, which includes Filtering, Linking,
Updating and much more.

Options
-------
The following options can be specified under ``.. needservice:: Excel`` and related directives.

file
~~~~~
The location of the spreadsheet file in the documentation directory. This option is required.
The file path must be an absolute path that starts with /, based on the **conf.py** directory.

Also, the accepted spreadsheet file type must have the ``.xlsx`` file extension.

prefix
~~~~~~
A string, which is taken as prefix for the need-id. E.g. ``EXCEL_IMPORT_`` --> ``EXCEL_IMPORT_005``.

query
~~~~~

A query string used to filter the data retrieved from the Excel service.
The query string must be a valid Python statement.

Example: This Python statement ``status == 'open' and assignee == 'Randy Duodu'`` can be used as:

.. code-block:: rst

   .. needservice:: Excel
      :query: status == 'open' and assignee == 'Randy Duodu'

.. note::
   When you use the query option, the filter in the value must match the column names (such as case sensitivity)
   in the spreadsheet file. For instance, if column name is **STATUS**, then use ``STATUS`` instead of ``status``
   in the filter (i.e. ``STATUS == 'closed'``).

header_row
~~~~~~~~~~
A number indicating the row in the spreadsheet which contains the names for each column. This option is required.
|br| **Default value**: 1

E.g. if ``:header_row: 2`` then retrieve the column names from row number **2** in our spreadsheet file.

start_row
~~~~~~~~~
A number which indicates the row to start retrieving data from in the spreadsheet file.
|br| **Default value**: 2

E.g. if ``:start_row: 15`` then we retrieve the data in our spreadsheet file, starting from row number **15**.

end_row
~~~~~~~
A number which indicates the row to end retrieving data from in the spreadsheet file. This option is required.

E.g. if ``:end_row: 20`` then we retrieve the data in our spreadsheet file, ending at row number **20**.

start_col
~~~~~~~~~~~
A number which indicates the column to start retrieving data from in the spreadsheet file.
|br| Default value: 1

E.g. if ``:start_col: 3`` then we retrieve the data in our spreadsheet file, starting from column number **3**.

end_col
~~~~~~~
A number which indicates the column to end retrieving data from in the spreadsheet file. This option is required.

E.g. if ``:end_col: 20`` then we retrieve the data in our spreadsheet file, ending at column number **20**.

.. note::

   You must ensure the numbers for both ``start_col`` and ``end_col`` will create the range
   to use in retrieving the appropriate data, that we can use in mapping between column names and Sphinx-Needs object
   options, as specified in your :ref:`conf_mapping`.
   For instance, if ``'mappings': {"id": ["sid"],}``, then the ``start_col`` and ``end_col`` should create a range
   which will retrieve data from the spreadsheet file that contains the **sid** column.

content
~~~~~~~
{% raw %}
``content`` takes a string, which gets interpreted as rst-code for the need-content area.
Jinja support is also available, so that service data is available and can be accessed like
``{{data.description}}``.

Example for the Excel service configuration:

.. code-block:: python

    excel_content = """
    {% if info in data %}
    {{data.info}}
    {% else %}
    {{data.description}}
    {% endif %}
    """

    needs_services = {
    'excel_config': {
        # ... some other values
        'content': excel_content
        }
    }

The set options for the ``needservice`` are available  under ``options``. Example:

.. code-block:: python

   my_content = """
   Data retrieved from file: {{options.file}}

   {{data.description}}

   {% if options.mapping.status == "is_open" %}
   **OPEN TASKS**
   {% endif %}
   """

{% endraw %}

Config
------
An ``Excel`` service configuration must be created inside your **conf.py** file.

.. hint::

   For details about most configuration options, please take a look into the
   :ref:`common configuration description <service_config>`.

The following documentation describes specific information for ``Excel`` service only.
{% raw %}

+ **file** : The file path to the spreadsheet file to use if the `file`_ option is not specified
  under the ``.. needservice:: Excel`` directive.
+ **start_row** : The row number to start retrieving data from in the spreadsheet file, if the `start_row`_ option
  is not specified under the ``.. needservice:: Excel`` directive.
+ **end_row** : The row number to end retrieving data from in the spreadsheet file, if the `end_row`_ option
  is not specified under the ``.. needservice:: Excel`` directive.
+ **start_col** : The column number to start retrieving data from in the spreadsheet file, if the `start_col`_ option
  is not specified under the ``.. needservice:: Excel`` directive.
+ **end_col** : The column number to end retrieving data from in the spreadsheet file, if the `end_col`_ option
  is not specified under the ``.. needservice:: Excel`` directive.
+ **mapping** : The field names of an Excel service object do not often map to option names of Sphinx-Needs.
  So mapping defines where a Sphinx-Needs option shall get its value inside the Excel service data. |br|
  mapping must be a dictionary, where the **key** is the needs object name and the **value** is either
  a Jinja string such as ``is_{{status}}`` or a list/tuple, which defines the location of the value in the retrieved
  Excel service data object.

  .. note::
     When you use a Jinja string as value, you must ensure the column names in the spreadsheet file,
     set as values for the mapping option, does not contain spaces because that will raise a
     `Jinja Template Syntax Error <https://jinja.palletsprojects.com/en/3.1.x/api/#jinja2.TemplateSyntaxError>`_.
     For example: Instead of the column name being ``CREATED AT`` use ``CREATED_AT``.

{% endraw %}

Example
-------

|ex|

Inside your ``conf.py`` file:

.. literalinclude:: /snippets/excel_config.py
   :language: python

Inside any ``rst`` file of your Sphinx project:

.. code-block:: rst

    .. req:: My first requirement
       :id: REQ_1
       :tags: main_example

       A need is a generic object which can become anything you want for your Sphinx documentation:
       a requirement, a test case, a user story, a bug, an employee, a product, or anything else.

    .. needservice:: excel_config
       :file: /services/spreadsheets/needs.xlsx
       :prefix: EXCEL_IMPORT_
       :start_row: 20
       :end_row: 21

    .. needservice:: excel_config_2
       :file: /services/spreadsheets/needs2.xlsx
       :prefix: EXCEL_IMPORT_2_
       :header_row: 21
       :start_row: 1
       :end_row: 4
       :start_col: 2

   .. needservice:: excel_config
      :file: /services/spreadsheets/needs.xlsx
      :query: STATUS == 'open' and ASSIGNEE == 'Randy Duodu'
      :start_row: 20
      :end_row: 21
      :debug:

.. container:: toggle

   .. container:: header

      **Show Output**

   .. req:: My first requirement
      :id: REQ_1
      :tags: main_example

      A need is a generic object which can become anything you want for your Sphinx documentation:
      a requirement, a test case, a user story, a bug, an employee, a product, or anything else.

   .. needservice:: excel_config
      :file: /services/spreadsheets/needs.xlsx
      :prefix: EXCEL_IMPORT_
      :start_row: 20
      :end_row: 21

   .. needservice:: excel_config_2
      :file: /services/spreadsheets/needs2.xlsx
      :prefix: EXCEL_IMPORT_2_
      :header_row: 21
      :start_row: 1
      :end_row: 4
      :start_col: 2

   .. needservice:: excel_config
      :file: /services/spreadsheets/needs.xlsx
      :query: STATUS == 'open' and ASSIGNEE == 'Randy Duodu'
      :start_row: 2
      :end_row: 21
      :debug:

