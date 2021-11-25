.. _dev:

sne dev
=======
The ``dev`` command contains subcommands, which are mostly used internally by the developer team to make things easier.

``sne dev --help``

.. _sne_dev_docker:

docker
------
Starts all docker-containers inside ``/docker`` with one single command.

``sne dev docker up``

Helpful to run tests and build the documentation against running external services like Jira or Codebeamer.
See also :ref:`contribute_docker` for some details about the docker configuration in ``Sphinx-Needs Enterprise``.

operation argument
~~~~~~~~~~~~~~~~~~
The operation argument must be one of ``up``, ``start``, ``stop``, ``down``.
They have the same meaning as they have for ``docker-compose``.

Please be aware that ``down`` will delete the container and therefore maybe also stored data.
This means e.g. for the Jira-container that the complete server registration and all data gets lost and you need
to start from scratch with the next run.
So ``stop`` is the better option for most docker containers.

browser option
~~~~~~~~~~~~~~
``sne dev docker up -b``

``-b / --browser`` will open for each found docker configuration a web browser with the related url.
