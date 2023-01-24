Changelog
=========

1.0.2
-----
**Released**: under developement

1.0.1
-----
**Released**: 24.01.2023

* Improvement: Added :ref: `ssl_cert_abspath` to allow self signed certificates for codebeamer service.

1.0.0
-----
**Released**: 26.09.2022

* Improvement: Added needs options check for creating needs from services import.
  `#40 <https://github.com/useblocks/sphinx-needs-enterprise/issues/40>`_
* Improvement: Works with Sphinx-Needs ``>=1.0.1`` (only).

0.1.4
-----
**Released**: 09.05.2022

* Improvement: Support of :ref:`cb_debug` option for Codebeamer added.
  `#25 <https://github.com/useblocks/sphinx-needs-enterprise/issues/25>`_
* Improvement: Added config option :ref:`conf_needs_enterprise_license_warn`.
* Bugfix: Invalid licenses do not write "warnings".
  `#35 <https://github.com/useblocks/sphinx-needs-enterprise/issues/35>`_
* Bugfix: Replacing ``m2r`` with ``m2r2``.
  `#43 <https://github.com/useblocks/sphinx-needs-enterprise/issues/43>`_


0.1.3
-----
**Released**: 29.11.2021

* Bugfix: Fixed some hard coded versions for dependencies

0.1.2
-----
**Released**: 29.11.2021

* Improvement: :ref:`conf_raw` and :ref:`conf_wiki2html` can be set in service configuration for Codebeamer.
* Bugfix: :ref:`cb_wiki2html` can be set to False.
  `#27 <https://github.com/useblocks/sphinx-needs-enterprise/issues/27>`_
* Bugfix: Not so strict dependency handling.

0.1.1
-----
**Released**: 25.11.2021

* Bugfix: Not so strict dependency handling.

0.1.0
-----
**Released**: 25.11.2021

* Improvement: Added :ref:`sne_export` for Elasticsearch.
* Improvement: Activates parallel build support.
  `#12 <https://github.com/useblocks/sphinx-needs-enterprise/issues/12>`_
* Improvement: Added :ref:`Azure service <service_azure>`.
* Improvement: Added :ref:`sne` subcommands: ``import``, ``render``, ``dev``.
* Improvement: Added :ref:`sne`.
* Improvement: Added :ref:`Codebeamer service <service_cb>`.
* Improvement: Added :ref:`Jira service <service_jira>`.
* Improvement:: Added :Ref:`cb_wiki2html` and :ref:`cb_raw` to service :ref:`service_cb`.
  `#11 <https://github.com/useblocks/sphinx-needs-enterprise/issues/11>`_
