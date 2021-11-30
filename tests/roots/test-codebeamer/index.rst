Test Codebeamer
===============

.. contents::
   :local:

Service calls
-------------

single item
~~~~~~~~~~~

.. needservice:: codebeamer_config
   :query: item.id = 1118
   :raw: False
   :wiki2html: True

All project items
~~~~~~~~~~~~~~~~~

.. needservice:: codebeamer_config
   :query: project.name IN ('my_project', 'another_project') and item.id != 1118
   :raw: True
   :wiki2html: True

Debug mode
----------
.. needservice:: codebeamer_config
   :query: item.id = 1118
   :debug:

