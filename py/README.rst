Porting of the Galen Framework API to Python.

This project is a porting the `Galen
Framework <http://galenframework.com/>`__ Java API to the Python
language.

The Python Galen API is made out of three parts. An example of usage is
shown below.

Galen Remote WebDriver
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

        driver = GalenRemoteWebDriver("http://localhost:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)

As explained above the API also expose a version of RemoteWebDriver API.

Check Layout API
~~~~~~~~~~~~~~~~

.. code:: python

        Galen().check_layout(driver, "specs/" + specs, included_tags, excluded_tags)

This part of the API resemble closely the checkLayout() method as it is
defined in the Java GalenApi class.

Hierarchical reports fluent API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

        TestReport("A galenpy test").add_report_node(info_node("Running layout check for: " + test_name).with_node(warn_node('this is just an example')).with_node(error_node('to demonstrate reporting'))).add_layout_report_node("check " + specs, check_layout_report).finalize()

The example above shows how to build a report in a hierarchical form by
adding report nodes in a fluent interface fashion. After chaining the
various nodes types such as info, warning or layout report, a call to
the method finalize() is done to create a test report that is added to
the list of reports.

Generating the report
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

       generate_galen_report('target/report')

At the end of the Galen Layout validation, the report is generated in
the given folder through the call of another Galen API method.

More examples
~~~~~~~~~~~~~

A separate project showing the usage of galenpy can be found at
`galen-sample-py-tests <https://github.com/valermor/galen-sample-py-tests>`__.
