.. _sne_import:

sne import
==========
``sne import`` allows the execution of configured need_services and stores the retrieved data in a ``needs.json`` file,
which can be used by ``.. needimport::``.

::

    $ sne import -c docs/conf.py jira -v 3.0.1 -r needs.json -o . -w

    Importing config from /home/daniel/workspace/sphinx/sphinx-needs-enterprise/docs/conf.py
    Using provider "jira" for given service jira

    URL: ``http://127.0.0.1:8081/rest/api/2/search``
    Query: project = PX
    Sending request:  Done
    Retrieved 2 element
    Version to use: 3.0.1
    Reusing needs.json: /home/daniel/workspace/sphinx/sphinx-needs-enterprise/needs.json
    Erasing existing data for version 3.0.1.

.. note::

   Please take into account that not all services are supporting all functions like ``sne import`` or ``sne export``.

   Take a look at the service badges on our main page, to figure out what a service currently supports.

use case
--------
``sne import`` can be used to retrieve and store baselines of external data at a specific point of time.
So instead of always getting the latest data via ``.. needservice:: jira`` during each build, ``sne import`` can
be used to request and store this data only once in a ``needs.json`` file.
This file can be stored inside your source version system, so that each developer works on the same data.
To get the data into your documentation, use ``.. needimport:: needs.json``.

For huge requests and big teams, this can reduce the number of requests against the external service dramatically and
it makes sure that each build is using the same data.

arguments
---------
``sne import`` takes only one argument, the name of the service to call.

service
~~~~~~~
A given service must be defined inside ``needs_services`` of a ``conf.py`` file.
By default ``sne`` looks into the current working directory for a ``conf.py`` file.
Use ``-c`` to specify another location.

The service key should start with the name of the tool, so that ``sne`` is selecting the internal driver automatically.
For instance: ``jira_my_server`` for ``JIRA`` or ``codebeamer123`` for ``Codebeamer``.

.. code-block:: bash

   sne import jira_my_server

options
-------

.. contents::
   :local:

-c / --conf
~~~~~~~~~~~
Can be used to specify the location of the ``conf.py`` file to use.

``sne import jira -c docs/conf.py``

Default: ``conf.py`` (in the current working directory)

-o/--outdir
~~~~~~~~~~~
The folder, under which the final ``needs.json`` file shall be created.
Will create not existing subfolders automatically.

``sne import codebeamer -o my_exports/2.0.1/``

Default: ``.`` (current working directory)

-q/--query
~~~~~~~~~~
Query to use for the service request.

``sne import jira -q "status != closed"``

Default: Taken from service config in ``conf.py``.

-r/--reuse
~~~~~~~~~~
Location of a ``needs.json`` compatible file, which data shall be copied/updated in the
final ``needs.json`` file.

``sne import codebeamer -r my_exports/2.0.1/needs.json``

Default: Not set

-v/--version
~~~~~~~~~~~~
The version, under which the data shall be stored in the ``needs.json`` file.

``sne import codebeamer -v 2.0.1``

Default: ``version`` attribute from ``conf.py``

-w/--wipe
~~~~~~~~~
If ``-r/--reuse`` is used, version specific data may contain data, which is not valid after an import. Maybe
because an issue got deleted, but its data is still available in the reused ``needs.json``.

Use ``-w / --wipe`` to delete all data for the version given by ``-v / --version`` before the newly imported
data is stored.

``sne import codebeamer -v 2.0.1 -w``

Default: Not set
