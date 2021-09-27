.. Sphinx-Needs Enterprise documentation master file, created by
   sphinx-quickstart on Tue Sep 21 09:02:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sphinx-Needs Enterprise's documentation!
===================================================

.. image:: /_static/sphinx-needs-enterprise-logo.png
   :align: center
   :scale: 40%

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**sphinx-needs tables**

.. req:: Test req
   :id: REQ_123
   :status: open

   This is an requirement.

.. req:: Test spec
   :id: SPEC_123
   :status: closed
   :links: REQ_123

   This is a **specification**.


**list table**

.. list-table::

   * - 123
     - 456
   * - abc
     - def

**text table**

+----------+----------+
| Header 1 | Header 2 |
+==========+==========+
| 1        | one      |
+----------+----------+
| 2        | two      |
+----------+----------+


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
