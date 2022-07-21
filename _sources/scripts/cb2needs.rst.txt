.. _cb2needs:

cb2needs
========

The script ``cb2needs`` (Codebeamer to Sphinx-Needs) creates a ``needs.json`` file based on
data coming from a codebeamer server.

Example: ``cb2needs --url my_codebeamer.com --user me --password secret -output needs.json``

For details about ``needs.json`` please read the related `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/>`_
documentation about
`the builder needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/builders.html>`_


Commandline interface
---------------------

With the installation of ``Sphinx-Needs-Codebeamer`` the script ``cb2needs`` got installed and was made available under
the currently used environment.

Type ``cb2needs --help`` to get some help and see available commands.

As script cb2needs
~~~~~~~~~~~~~~~~~~
Use the script ``cb2needs`` to get a json file, which can be used via directive :ref:`needsimport <needs:needimport>`
from the `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__ extension to filter and import
needed data into the right place of your Sphinx documentation.

**Example**:

Inside your project ``/docs`` folder run
``cb2needs --url my_codebeamer.com --user me --password secret -output needs.json``.

This will create the file ``/docs/needs.json``.

Then inside any rst file add:

.. code-block:: rst

   My open issues from codebeamer:

   .. needimport:: /needs.json
      :filter: status == "open"

For details please take a look into :ref:`cb2needs` and :ref:`needsimport <needs:needimport>`.
