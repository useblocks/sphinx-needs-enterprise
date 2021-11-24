.. _service_cb:

Codebeamer
==========

The ``Codebeamer`` service synchronizes
data between `codebeamer <https://codebeamer.com/>`_ from `Intland <https://intland.com/>`_ and the
Requirement Engineering extension `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ from
`useblocks <https://useblocks.com>`_.

The implementation is based on the :ref:`services mechanism <needs:services>` of
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__.

The ``Codebeamer`` service allows to retrieve external data during documentation build and
to create Sphinx-Needs objects based on this data.
After the created Sphinx-Needs objects support every function from
`Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`__, which includes Filtering, Linking,
Updating and much more.

Options
-------
The following options can be used inside ``.. needservice:: Codebeamer`` and related directives.

query
~~~~~
A query string, which must be valid to `cbQL <https://codebeamer.com/cb/wiki/871101>`_.

prefix
~~~~~~
A string, which is taken as prefix for the need-id. E.g. ``CB_IMPORT_`` --> ``CB_IMPORT_005``.

.. _cb_raw:

raw
~~~
If set to "True", the description content gets presented inside a code-block and is not handled as rst-valid text
anymore. Use it to avoid sphinx build errors, is the item description is based on wiki or html syntax.

Default: False

.. _cb_wiki2html:

wiki2html
~~~~~~~~~
If set to "True", wiki-based item content gets transformed to html and is presented in a
``.. raw:: html`` directive.

Default: True

If ``raw`` is set as well, content gets transformed to HTML, but is presented inside a ``code-block``.

Config
------
A Codebeamer service configuration must be created inside your ``conf.py`` file.

.. hint::

   For details about most configuration options, please take a look into the
   :ref:`common configuration description <service_config>`.

The following documentation describes service specific information for ``Codebeamer`` only.

endpoint
~~~~~~~~
Default value for ``Codebeamer`` services is ``/rest/v3/items/query``.

See also :ref:`conf_endpoint` for more details.

url
~~~
Please see :ref:`conf_url` for details.


Example
-------
Inside your ``conf.py`` file:

.. literalinclude:: /snippets/azure_config.py
      :language: python

Inside any ``rst`` file of your Sphinx project:

.. code-block:: rst

   .. needservice:: codebeamer_config
       :query: project.name IN ('my_project', 'another_project')
       :prefix: CB_IMPORT

   .. needtable::
      :filter: "CB_IMPORT" in id

**Result**

{% if on_ci != true %}

.. needservice:: codebeamer_config
   :query: project.name IN ('my_project', 'another_project') and type = 'Requirement' and status = 'Draft'
   :prefix: CB_IMPORT_

.. needtable::
   :filter: "CB_IMPORT" in id
   :columns: id, title, status, type
   :style: table

{% else %}
.. hint::

   The below examples are just images, as no Codebeamer instance was available during documentation build.

.. image:: /_images/cb_example.png
   :align: center
   :width: 60%

.. image:: /_images/cb_table.png
   :align: center
   :width: 60%

{% endif %}



