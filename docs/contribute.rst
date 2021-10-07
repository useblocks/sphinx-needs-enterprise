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


External services
-----------------
For some services like CodeBeamer, there are open Docker Images available, which can be used
to test ``Sphinx-Needs Enterprise`` and to build the documentation with active data synchronization.

To start the needed service, go to ``/docker/<service>`` and run ``docker-compose down && docker-compose up -d``.

Docker configurations are available for:

* **CodeBeamer**: ``/docker/codebeamer``

