Installation
============

github
------

Run::

    git clone git@github.com:useblocks/sphinx-needs-enterprise.git
    cd sphinx-needs-enterprise
    pip install .

PyPi
----

Run ``pip install sphinx-needs-enterprise``.

Registration
------------
After installation, the extensions need to be registered in the ``conf.py`` file:

.. code-block:: python

    extensions = [
        # ... other extensions
        'sphinx_needs_enterprise']

License activation
------------------
If a license for commercial projects is available, this can be set in ``conf.py`` via:

.. code-block:: python

   needs_enterprise_license = "ABCDE-FGHIJ-KLMNO-PQRST"

For license details, please read :ref:`license`.
