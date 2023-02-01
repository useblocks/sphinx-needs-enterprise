.. _sne:

sne script
==========
The ``sne`` (Sphinx-Needs Enterprise) script bundles all cli commands, which are available for
``Sphinx-Needs Enterprise``.

It's main goal is to support the execution of tasks outside of Sphinx itself,
e.g. for storing data in json files during CI operations.

To use it, ``Sphinx-Needs Enterprise`` must be installed. Then the ``sne`` command is automatically available on your
terminal:

.. command-output:: sne --help


.. toctree::
   :maxdepth: 1
   :caption: Available commands

   import
   export
   render
   dev

.. note::

   Please take into account that not all services supports all functions like ``sne import`` or ``sne export``.

   Take a look at the service badges on our main page, to figure out what a service currently supports.






















