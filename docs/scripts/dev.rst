.. _dev:

sne dev
=======
The ``dev`` command contains subcommands used internally by the developer's team to make things easier.

``sne dev --help``

.. _sne_dev_docker:

docker
------
Starts all docker-containers inside ``/docker`` with one single command.

``sne dev docker up``

It is helpful to run tests and build the documentation against running external services like Jira or Codebeamer.
See :ref:`contribute_docker` also for some details about the docker configuration in ``Sphinx-Needs Enterprise``.

operation argument
~~~~~~~~~~~~~~~~~~
The operation argument must be one of these: ``up``, ``start``, ``stop``, ``down``.
These arguments have the same meaning as the ones for``docker-compose``.

Please be aware that ``down`` will delete the container and therefore you must store data.
For instance; if you use the ``down`` argument in a Jira-container, the complete server registration and all data gets lost.
With the next run, you need to start everything from scratch.
So ``stop`` is the better option for most docker containers.

browser option
~~~~~~~~~~~~~~
``sne dev docker up -b``

``-b / --browser`` will open for each found docker configuration a web browser with the related url.
