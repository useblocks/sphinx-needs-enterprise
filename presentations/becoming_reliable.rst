.. Sphinx-Needs Enterprise License documentation master file, created by
   sphinx-quickstart on Mon Sep 27 14:25:43 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Becoming reliable
=================
.. image:: ../docs/_static/sphinx-needs-enterprise-logo.png
   :scale: 30%

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/white_small_move.html


What is Sphinx-Needs!
---------------------
| A highly customizable, free and open
| **Lifecycle Management toolbox for developers**
| to enhance their productivity to a new maximum.

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/colored_small_move.html

Features
~~~~~~~~

* Objects of different types
* Link objects
* Analyse objects with tables, flow and pie charts
* Define custom options, layout and styles
* Automate data calculation
* Im/Export data from/to external systems

➔ All as Docs-As-Code

Input
~~~~~
.. code-block:: rst


   Here is a requirement for **code quality**:

   .. req:: Python code must be PEP8 compliant
      :id: REQ_PY_PEP8
      :status: closed
      :tags: python, quality
      :style: yellow, red_border

      The python code of our product must follow
      `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.



Result
~~~~~~

Here is a requirement for **code quality**:

.. req:: Python code must be PEP8 compliant
   :id: REQ_PY_PEP8
   :status: closed
   :tags: python, quality
   :style: yellow, red_border

   The python code of our product must follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.

Analysis
~~~~~~~~
``.. needtable::``

.. needtable::
   :style: table

Analysis 2
~~~~~~~~~~
``.. needflow::``

.. image:: /_static/needflow_example_1.svg

Analysis 3
~~~~~~~~~~
``.. needpie::``

.. needpie::
   :labels: Requirements, Specifications, Tests
   :shadow:
   :explode: 0.2, 0, 0

   type == 'req'
   type == 'spec'
   type == 'test'

Business Model
--------------
Why is it needed?

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/white_small_move.html

Challenges
~~~~~~~~~~
Sphinx-Needs is mainly used by process driven companies.

Users may not be allowed to support Open Source projects.

Users don't contribute during after-work hours.

➔ Tough community building

Challenges 2
~~~~~~~~~~~~
Fast reaction time may be needed.

Problems may be company specific and can't be openly discussed.

Maintenance shall be independent from customers and projects.

| ➔ An ongoing income is needed to get
| **1-2 full-time developers** on it.

Sphinx-Needs Enterprise
-----------------------
A collection of tools and scripts to embedded Sphinx-Needs inside companies tool environments.

➔ One-Stop-Shop of Truth

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/white_small_move.html

.. revealjs-break::
   :notitle:


.. image:: ../docs/_static/sphinx-needs-enterprise-content.png


Connectors
~~~~~~~~~~
Import and Export of data from:

* CodeBeamer
* Azure Boards
* Jira
* GitHub Enterprise
* ... any other tool with a REST API

File Handlers
~~~~~~~~~~~~~
Work with data formats like:

* ReqIF (e.g. supported by DOORS)
* Ms Excel/Word
* ... company specific tools

Databases
~~~~~~~~~
| Store, Retrieve and Analyse
| current and historical data:

* Open Needs DB
* ElasticSearch
* ... any other document-based DB

Analytics
~~~~~~~~~
Send and show metrics on external dashboards:

* ElasticSearch / Kibana
* Splunk
* Grafana

Viewers
~~~~~~~
Filter and analyse data across documentations and projects:

* Standalone needs viewer
* Embedded viewer for Sphinx documentations
* VS Code viewer
* ... any other IDE with Extension support

Editors
~~~~~~~
Write, link and configure Needs with technical support:

* VS Code Language Server
* Intellij / PyCharm Language Server

Theme
~~~~~
* Professional HTML and PDF themes for documentations and presentations
* Additional areas for information

  * Static links to other tools
  * Badges for real-time data (e.g. build status)

* Enhancement for huge documentations:

  * Long, complex TOC and sidebars
  * Search across documentations

Additional solutions
~~~~~~~~~~~~~~~~~~~~
* Needs Comment Server
* Sphinx-Metadata (Page specific data)


Business Source License
-----------------------
| An eventually Open Source license

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/white_small_move.html

Eventually?
~~~~~~~~~~~

* Open code, docs and issue tracker all the time.
* It's **free** for ALL.

  * Except you fulfill the usage limitations (commercial usage).

* It becomes automatically **Open Source** after 4 years.

  * Released under MIT.
  * No usage limitations anymore.

License change example
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :stub-columns: 1
   :align: center

   - * Usage
     * | Release 2021
       | 2021 - 2025
     * | Release 2021
       | 2025 - ...
   - * Private
     * BSL
     * MIT
   - * Commercial
     * Commercial License
     * MIT

Sphinx-Needs stays MIT, forever!

Secured usages?
~~~~~~~~~~~~~~~

* Yes, but with textual hints only.

  * During installation.
  * In outputs, logs and maybe in results.

* Software will work all the time.
* But with on-the-fly license checks.

Offers
------

.. revealjs-section::
   :data-background-iframe: _static/dynamic_background/white_small_move.html


| **Whatever is needed**
| Licenses, Support, Trainings
| and Development Service

License
~~~~~~~
* Access to enterprise features
* Support ongoing development of Sphinx-Needs
* Influence issue priorities
* Support via issue tracker

Support contract
~~~~~~~~~~~~~~~~
* Faster reaction time and bug fixes
* Company and user specific solutions
* SLA possible
* Additional contact via email, telephone and online meetings

Trainings
~~~~~~~~~
* Sphinx, Sphinx-Needs and Sphinx-Needs Enterprise
* For beginners, power users and developers
* Company specific integrations

`sphinx-needs.com/trainings <https://www.sphinx-needs.com/trainings>`_

Development service
~~~~~~~~~~~~~~~~~~~
* Company specific concepts and solutions
* Development, Maintenance, Operations
* From small scripts to complete tool chains
* Working inside company networks
* Responsible for topics, not only tech. solutions
* Temporary on-site contact

License types
-------------

* **Floating license**
* User based license¹
* Node based license¹

¹ if requested

Floating license
~~~~~~~~~~~~~~~~

.. math::

   \tiny{
   \text{ Licenses } = \text{ Users } *
   \frac {  \text{ User builds}} { \text{ Working time }}
   * \text{ Build duration}
   }

**Example**

.. math::

   50
   * \frac {6 \tiny{\text { Builds}}} { 10h * 60}
   * 5min
   = 2.5 => \text{ 3 Licenses }

Thanks
------

.. image:: ../docs/_static/sphinx-needs-enterprise-logo.png
   :scale: 20%

Example Data
~~~~~~~~~~~~

1
~

.. spec:: Use flake to check PEP8
   :id: SPEC_FLAKE
   :links: REQ_PY_PEP8
   :status: closed

2
~

.. test:: Quality tests
   :id: TEST_SW_QUALITY
   :links: SPEC_FLAKE
   :status: open

   Provides some test cases to check if "dirty" code
   gets detected by Flake8, which was introduces by
   :need:`SPEC_FLAKE`
