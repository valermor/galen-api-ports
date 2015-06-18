Galen API Ports
===============
[![Build Status](https://travis-ci.org/valermor/galen-api-ports.svg?branch=master)](https://travis-ci.org/valermor/galen-api-ports)


_Galen API Ports_ is an attempt to port the [Galen Framework](http://galenframework.com "Galen's Homepage") API to languages other than Javascript and Java, which are the ones officially supported.
The project is mean to provide a framework to port the Galen Java API into any of that languages that are supported by Apache Thrift.
At the moment, only porting to Python is implemented under the name _galenpy_ (read on).

##Why
At my current job, most teams speak Python. Maintaining a Java project was becoming expensive and not a scalable option. This is also true in many other workplaces.
I thought providing a solution would help other people like me who want to use the Galen Framework but still would like to stick to their own language.

That was also a lot of learning and fun!

If you are interested to extend the tool into a language that is not supported (Java, JavaScript and Python), shoot me an email to me and we can have a chat on how you can start on it.

##License
_Galen API Ports_ is licensed under the Apache Software License 2.0 provision.

##Architecture and implementation details
The porting of the Java API is based on a simple idea. Through an RPC we expose the same functionality as the native API to any other language implementation.

The RPC we use is [Apache Thrift](https://thrift.apache.org/).
A Thrift Java Server wraps the Galen Java API, while other languages APIs implement Thrift clients.
Currently, only a Python client exists, namely the [galenpy](https://pypi.python.org/pypi/galenpy) API. Both server and client currently live in the same project.

![API port concept](/galen-api-ports.png)

The services Galen APIs provide can be divided into two sets:

- Hierarchical reports creation

- Layout validation based on Galen Spec language

Additionally, the ported API must expose the WebDriver API. The reason is that Galen API needs a reference to the WebDriver instance to perform actions on the page under test.
A custom _Jsonwire over Thrift_ implementation allows to expose Remote WebDriver by the client API.

###Json over Thrift Remote WebDriver
On the client side, the Jsonwire protocol is implemented inside a customized RemoteConnection which marshalls/unmarshalls Jsonwire commands to and from the Java RemoteWebDriver end via Thrift.
When the server receives those commands, it unpackages and executes them through the CommandExecutor of the RemoteWebDriver instance wrapped inside the server.

###Server lifecycle
The Thrift server is able to serve clients concurrently.
Among the other things, one of the problems that is solved in the porting is making sure that the server is always available when tests are running and it quits when idle.
On normal usage of the API, the first time the Galen API is called the server should be started. The server will be running until report is generated.
As some test implementations might want to have control of the server lifecycle, an environment variable exists that disable launching of the server by tests:

```
    SERVER_ALWAYS_ON=True
```

This assumes, Galen API service should be launched manually with the below command:

```
    java -jar <path_to_server_jar>/galen-api-server.jar -r <port>
```

###Limitations
At the moment, you can run your tests only against a Selenium Grid, i.e. no local driver is supported.

###Building the tool
####Assembly server jar###
Thrift language files are not part of the repo. They get generated on build time from _galen_api.thrift_.

Building and assembling of the Java Server is done automatically by _assemble_java_server.sh_.

####Configure Java server log###
Log configuration file 'simplelogger.properties' inside resource folder contains logging configuration.
The file gets copied into Java classpath on assembly step before.

###Distributing galenpy##
Distribution of galenpy to PyPI is automated via the distribute_galenpy.sh script.
Running the script will package galenpy for distribution into PyPI. Notice the script also distributes a copy of the source along with a Python Wheel.

```
    distribute_galenpy.sh -no-upload
```

## galenpy API

[![PyPI](https://img.shields.io/pypi/wheel/galenpy.svg)]()
[![PyPI](https://img.shields.io/pypi/v/galenpy.svg)]()
[![PyPI](https://img.shields.io/pypi/dm/galenpy.svg)]()


The Python Galen API is made out of three parts. An example of usage is shown below.

### Galen Remote WebDriver
```python
    driver = GalenRemoteWebDriver("http://localhost:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
```
As explained above the API also expose a version of RemoteWebDriver API.

### Check Layout API
```python
    Galen().check_layout(driver, "specs/" + specs, included_tags, excluded_tags)
```
This part of the API resemble closely the checkLayout() method as it is defined in the Java GalenApi class.

### Hierarchical reports fluent API
```python
    TestReport("A galenpy test").add_report_node(info_node("Running layout check for: " + test_name).with_node(warn_node('this is just an example')).with_node(error_node('to demonstrate reporting'))).add_layout_report_node("check " + specs, check_layout_report).finalize()
```
The example above shows how to build a report in a hierarchical form by adding report nodes in a fluent interface fashion.
After chaining the various nodes types such as info, warning or layout report, a call to the method finalize() is done to create a test report that is added to the list of reports.

### Generating the report
```python
   generate_galen_report('target/report')
```
At the end of the Galen Layout validation, the report is generated in the given folder through the call of another Galen API method.

### More examples
A separate project showing the usage of galenpy can be found at [galen-sample-py-tests](https://github.com/valermor/galen-sample-py-tests).
