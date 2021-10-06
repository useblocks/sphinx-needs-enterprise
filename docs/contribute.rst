Contribute
==========

Doc build
---------
On project root: ``make docs-html``

Under ``/docs``: ``make html``

Use local codebeamer instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To build the documentation with local codebeamer support you must set the tag ``local_dev``.
This can be achieved by directly using ``sphinx-build`` inside ``/docs`` folder:
``sphinx-build -a -E -b html . _build/html -t local_dev``

This will execute ``needservice`` request during documentation build, what is not possible on ReadTheDocs servers
or when no codebeamer instance is available.

RST code, which shall be executed with the tag ``local_dev`` only, must be added like this to the documentation:

.. code-block:: rst

    .. only:: local_dev

       .. needservice:: codebeamer
          :query: project.name IN ('my_project', 'another_project')
