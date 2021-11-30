.. _license:

License
=======
``Sphinx-Needs Enterprise`` is released under the ``BSL 1.1``, the Business Source License.
Which mostly means the usage is free for private projects, but commercial projects need to purchase a license.

To obtain a license key please visit
`sphinx-needs.com <https://sphinx-needs.com>`_ or get in contact with
`useblocks <https://useblocks.com>`_, the company behind this extension.

Config
------
A license key must be set via the config option ``needs_enterprise_license`` in the ``conf.py`` file
of a Sphinx project.

The value of ``needs_enterprise_license`` must be a string in the format ``ABCDE-FGHIJ-KLMNO-PQRST``.

If no license key is set for ``needs_enterprise_license``, the **private mode** is activated and Sphinx-Needs
Enterprise can be used for private, none commercial projects.

With no license key set, you will get some hints during startup and end of the build.
Mainly telling you that **private mode** is active and that it would be nice to support Sphinx-Needs, if used
for commercial projects.

This hints / log entries can be deactivated by setting ``needs_enterprise_license = "PRIVATE"``.
In this case, only a one-liner will be printed that Sphinx-Needs Enterprise is licensed for private projects.

.. _conf_needs_enterprise_license_warn:

needs_enterprise_license_warn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If ``True`` SNE will write warnings, if something went wrong with the license, e.g. no floating-license is
available right now.

Default: False


License check workflow
----------------------
As all licenses are Floating licenses, they can be used by multiple users, but not in parallel.
The amount of parallel usages is defined by purchased keys per license.

The license key status gets checked during initialisation of the Sphinx-Needs Enterprise extension.

If ``needs_enterprise_license`` is not set or set to ``PRIVATE``, the **private mode** gets directly activated
and no request to the external license server in the cloud is made.

If a license is set, then the license server of `Cryptolens <https://cryptolens.io/>`_ is asked to validate the
license key.

During license validation, the current license gets blocked by the current machine for 5 minutes.
If the build takes longer as 5 minutes, this block gets renewed every 5 minutes.

After the build has finished (and was not interrupted by the user or has crashed) the blocked license gets freed and is
immediately available for the next machine.

If all available license keys are used, Sphinx-Needs Enterprise waits 5 seconds until the license server is asked again.
After 3 unsuccessful attempts, the license is set into **private mode** for the current build and the builds goes on.
If this happens more then 2-3 times a day, please consider to request additional license keys.

.. hint::

   For sensitive company networks with no internet connection or other security concerns, a local license server can be
   provided with no extra costs.

FAQ
---

.. dropdown:: Why is it not free for all?

    ``Sphinx-Needs`` and related extensions are mostly used by process driven companies.
    And so most of our users and contributors must follow company internal rules, if they want to contribute to an
    Open-Source project.
    They also use Sphinx-Needs mostly during their daily work, so motivation to spend additional time
    on it after work is low.

    This makes it hard for the ``Sphinx-Needs`` community to gain enough contributors, even if the amout of users is
    quite high and most of them are developers.

    So we have created ``Sphinx-Needs Enterprise``, which shall help to retrieve some kind of money back from companies,
    which earn or save money thanks to ``Sphinx-Needs`` and which have a special interest in the solutions provided by
    ``Sphinx-Needs Enterprise``.

    The money gets completely spent on development power for ``Sphinx-Needs`` and related extensions.
    And we hope that one day a fulltime engineer can work on it thanks to the license fees.

.. dropdown:: Any chance of a discount?

    Sure, we support startups, small companies, research and academic use cases.

    Just get in touch with us at `useblocks <https://useblocks.com>`_.

License Text
------------

.. literalinclude:: /../LICENSE
