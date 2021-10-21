.. _contribute:

Contribute
==========

Doc build
---------

With external services
~~~~~~~~~~~~~~~~~~~~~~
This build is for systems, which have e.g. a running CodeBeamer instance available, so that real data can
be fetched during build.

On project root: ``make docs-html``

Under ``/docs``: ``make html``

Without external services / CI Build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the documentation build shall act like it is performed on our used CI system (github actions),
an environment variable must be set. The build will then contain images instead of trying to reach
external services during build.

On project root: ``make ci-docs-html``

Under ``/docs``: ``ON_CI=true make html``


.. _contribute_docker:

External services via docker
----------------------------
For some services like CodeBeamer, there are open Docker Images available, which can be used
to test ``Sphinx-Needs Enterprise`` and to build the documentation with active data synchronization.

To start the needed service, go to ``/docker/<service>`` and run ``docker-compose down && docker-compose up -d``.

You can also use the ``sne`` script to start **all available containers** with one command for you:
``sne dev docker up``. See: :ref:`sne_dev_docker` for details.

Codebeamer
~~~~~~~~~~
Open a terminal and switch folder to ``/docker/codebeamer``.

Then run ``docker-compose down && docker-compose up -d``.

After everything is running, open a browser with this address http://127.0.0.1:8080/.

Login data is:
:username: bond
:password: 007

Jira
~~~~
Open a terminal and switch folder to ``/docker/jira``.

Then run ``docker-compose up -d``.

After everything is running, open a browser with this address http://127.0.0.1:8081/.

You will be asked several questions and need to login with an atlassian cloud account to create an evaluation
license for your specific server.

To test the REST API open http://127.0.0.1:8081/rest/api/2/search in a browser to get json based content, which
includes all available issues.

The JIRA container should be stopped with ``docker-compose stop``. Use ``stop`` instead of ``down``, as ``down`` will
delete the container, together with the internal config and database.
So after using ``down`` you must register your server and add all the data again.
