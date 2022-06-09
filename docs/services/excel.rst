.. _service_excel:

Excel
=====
Imports data from spreadsheets to Sphinx-project using Sphinx-Needs and creates Sphinx-Needs objects on the fly during build time.

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
