.. _sne_export:

sne export
==========
``sne export`` allows to export data from ``needs.json`` to an external service::

    $ sne export -c docs/conf.py  elasticsearch_config

    Importing config from /home/.../docs/conf.py
    Using provider "elasticsearch" for given service elasticsearch_config

    Reading json data: Done
    Connection to Elasticsearch url: ``http://127.0.0.1:9200``
    Creating index needs
    ████████████████████████████████████████████████████████████████████████████████ 100% | Uploading need JIRA_PX-2:
    Uploaded 8 elements.

Each need gets automatically a new option named ``uploaded_at``, which has the current date and time as value.

.. note::

   Please take into account that not all services are supporting all functions like ``sne import`` or ``sne export``.

   Take a look on the service badges on our main page, to figure out what is currently supported.

arguments
---------
``sne export`` takes only one argument, the name of the service to call.

service
~~~~~~~
A given service must be defined inside ``needs_services`` of a ``conf.py`` file.
By default ``sne`` looks into the current working directory for a ``conf.py`` file.
Use ``-c`` to specify another location.

The service key should start with the name of the tool, so that ``sne`` is selecting the internal driver automatically.
For instance: ``elasticsearch_my_server`` for ``Elasticsearch``.

.. code-block:: bash

   sne export elasticsearch_my_server

options
-------

.. contents::
   :local:

-c / --conf
~~~~~~~~~~~
Can be used to specify the location of the ``conf.py`` file to use.

``sne export elasticsearch_my_server -c docs/conf.py``

Default: ``conf.py`` (in the current working directory)

-j / --json
~~~~~~~~~~~
Location of a ``needs.json`` compatible file, which data shall exported to the service.

``sne export elasticsearch -j docs/needs.json``

Default: ``needs.json``

-v / --version
~~~~~~~~~~~~~~
Version to take from the given ``needs.json`` file.
All needs under this version will get exported.

``sne export elasticsearch -v 3.0.1``

Default: ``current_version`` value set inside needs.json file


-x / --extra
~~~~~~~~~~~~
Additional data, which shall be set on each exported need.

``sne export elasticsearch -x branch main``

Default: None

-h / --hours
~~~~~~~~~~~~
Allows to manipulate the ``updated_at`` value of each need.

Useful to test uploads with the same data but with different timestamp.

Allows positive and negative floating numbers (e.g. '2' or '-3.5'), which will be added or subtracted from current
time.

``sne export elasticsearch -h 2.5``

Default: 0

-s / --skip
~~~~~~~~~~~
Skips every x element during export. So if 10 needs are defined inside ``needs.json'' and ``skip = 2``, then ony ``5``
needs get exported.

Useful also only for tests, to scaling down the test data to export.

``sne export elasticsearch -s 5``

Default: None

