.. _contribute:

Contribute
==========

Code linting
------------
Use ``make format`` to run ``black`` on your code, which should fix most of possible linter errors.

To run all our configured linter, run ``make lint``.

Testing
-------
As ``SNE`` is highly using external services, some tests need a running and correctly preconfigured service instance.
But these service instances are not available during CI tests, so that external calls needs to be mocked.

If a test needs a running external service, e.g. to debug things easier, mark it like this::

    @pytest.mark.sphinx(testroot="codebeamer")
    @pytest.mark.cb_needed  # Uses marker "cb_needed"
    def test_codebeamer(app):
        app.build()

New markers must be registered in ``pytest.ini``.

Local tests should be run with ``pytest -m local``. You can use ``make test-local`` to run all tests this way.


Currently supported are::

* ``local``: Test that can be run locally. May require external resources
* ``external_resource``: Marks tests that require external resources.
* ``cb_needed``: local tests
* ``cb_needed``: Needs a running codebeamer server.
* ``cb_docker_needed``: Needs a running docker codebeamer server.
* ``ci_test``: Marks remote tests that are executed only in GitHub workflows.
* ``sphinx``: testing sphinx.

Only tests marked with `ci_test`` get executed during CI runs. For local tests use ``make test-local``, this invokes
``poetry run pytest -v tests -m local``. Please be aware that local test can sometimes require locally running docker
containers. Local tests requiring external resources can be disabled by running ``make test-no-ext``

So if you register a new marker, please update also the related Makefile command.

All unmarked tests must be callable without the need to use any external resources.

Sphinx support
~~~~~~~~~~~~~~
How to run test cases based on a Sphinx project is nearly undocumented by Sphinx itself.
Some information can be found here: https://github.com/sphinx-doc/sphinx/issues/7008



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

External services
-----------------
For some services like CodeBeamer, there are open Docker Images available, which can be used
to test ``Sphinx-Needs Enterprise`` and to build the documentation with active data synchronization.

To start the needed service, go to ``/docker/<service>`` and run ``docker-compose down && docker-compose up -d``.

You can also use the ``sne`` script to start **all available containers** with one command for you:
``sne dev docker up``. See: :ref:`sne_dev_docker` for details.

Codebeamer via docker
~~~~~~~~~~~~~~~~~~~~~
Open a terminal and switch folder to ``/docker/codebeamer``.

Then run ``docker-compose down && docker-compose up -d``.

After everything is running, open a browser with this address http://127.0.0.1:8080/.

Login data is:
:username: bond
:password: 007

To use the current documentation with the new codebeamer instance, you should create a project based on the ``agile``
template. In this case some elements, like issues, get automatically created and the used filters inside this
documentation should already match some of them.

Jira via docker
~~~~~~~~~~~~~~~
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


Azure DevOps
~~~~~~~~~~~~
``Azure DevOps`` can only be used as cloud service. A local installation is not possible.
Luckily there is a free plan available, so for testing create an account via
https://azure.microsoft.com/en-us/services/devops/.

For a documentation build of ``Sphinx-Needs Enterprise`` you should set the env vars
``NEEDS_AZURE_URL`` and ``NEEDS_AZURE_TOKEN`` with your specific data.
They will overwrite the config set in ``docs/conf.py``.


ElasticSearch and Kibana
~~~~~~~~~~~~~~~~~~~~~~~~
Open a terminal and switch folder to ``/docker/elasticsearch``.

Then run ``docker-compose up -d``. This will start an ``ElasticSearch`` server and a ``Kibana`` server.

``ElasticSearch`` is listening on Port ``9200`` and ``9300``.
``Kibana`` on port ``5601``.

To test everything, open http://127.0.0.1:5601 or http://127.0.0.1:5601/app/home#/tutorial_directory/sampleData
to add some sample data.




