Test Excel Importer
===================

.. contents::
   :local:

Service calls
-------------

Single item
~~~~~~~~~~~

.. needservice:: excel_config
   :start_row: 20
   :end_row: 20

Multiple items
~~~~~~~~~~~~~~

.. needservice:: excel_config
   :start_row: 2
   :end_row: 21
   :query: STATUS == 'progress' and ASSIGNEE == 'Marco Heinemann'

Debugging Excel Service
~~~~~~~~~~~~~~~~~~~~~~~

.. needservice:: excel_config
   :start_row: 2
   :end_row: 4
   :debug:
