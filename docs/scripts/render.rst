
.. _render:

sne render
==========
``render`` uses a Jinja2-Template and combines it with data from a ``needs.json`` file to generate a new output file,
which can be a rst-file, a html-report, custom xml, whatever.

``sne render``

options
-------
``sne render -j needs.json -t my_template.rst -o output.rst``

.. contents::
   :local:

-j / --json
~~~~~~~~~~~
Defines a relative file to a json file, which can be a ``needs.json`` file.

Default: ``needs.json`` in the current working directory

-t / --template
~~~~~~~~~~~~~~~
Relative path to a jinja2 template file.

If it is not set, an internal template is used to provide a fast way to test it.
See :ref:`default_template` for details.

Default: Sphinx-Needs Enterprise internal template

-o / --output
~~~~~~~~~~~~~
Relative path to an output file, which gets overwritten, if it already exists.

Default: ``needs.rst`` in the current working directory

Own template file
-----------------
{% raw %}
The template is using `Jinja <https://jinja.palletsprojects.com/en/3.0.x/>`_ as template language.

The complete data from the loaded json file is available under the name ``data``.
Example for getting the project name of a loaded ``needs.json`` use ``{{ data.project}}``.

Also ``{{ now }}`` can be used to get the current datetime.

For some ideas of how a report template may look like, please take a look into our :ref:`default_template`.

{% endraw %}

.. _default_template:

Default template
----------------

.. literalinclude:: ../../sphinx_needs_enterprise/templates/needs.rst.template
   :language: jinja

**Result Example**

.. code-block:: rst

    Sphinx-Needs Enterprise
    =======================


    | Report created: 2021-10-21 11:33:44.107829
    | Data exported: 2021-10-21T11:31:06.176901
    | Versions found: 1
    | Current version: 1.0.0

    **Versions**:

    .. contents::
       :local:


    1.0.0
    -----

    | Needs: 2
    | Created: 2021-10-21T11:31:06.176874

    Needs
    ~~~~~


    .. spec:: Built in GPS-System
       :id: CB_1018
       :status: Draft

       Codebeamer Link to Issue 1018 ``<http://127.0.0.1:8080/issue/1018>``

       Example content




    .. spec:: Navigation system
       :id: CB_1091
       :status: Draft

       Codebeamer Link to Issue 1091 ``<http://127.0.0.1:8080/issue/1091>``

       Example content

