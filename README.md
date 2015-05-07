Galen API Ports
===============
[![Build Status](https://travis-ci.org/valermor/galen-api-ports.svg?branch=master)](https://travis-ci.org/valermor/galen-api-ports)


_Galen API Ports_ is an attempt to port the [Galen Framework](http://galenframework.com "Galen's Homepage") API to languages other than Javascript and Java, which are the ones officially supported.
At the moment, only porting to Python is provided.

##License
_Galen API Ports_ is licensed under the Apache Software License 2.0 provision.

##Architecture
The idea is simple. Galen Java APIs are made available to other languages through an RPC implementation.
The RPC is based on [Apache Thrift](https://thrift.apache.org/).
A Thrift Java Server calls the Galen Java API, while clients implemented in other languages are free to expose their own API implementation.
The services Galen APIs provide can be divided into two groups:
- Hierarchical reports creation
- Layout validation based on Galen Spec language

Currently, only a Python client exists. Both server and client live in the same project.

##Json over Thrift Remote WebDriver
In a typical Galen layout test, some interactions (via the WebDriver APIs) would prepare the page under test for a layout inspection.
This has the implication that also the functionality exposed by the WebDriver instance have to go through the Thrift interface.
This is accomplished through the implementation of a Jsonwire over Thrift Remote WebDriver Interface.
In a nutshell, the Jsonwire protocol is implemented inside a customized RemoteConnection which marshalls/unmarshalls Jsonwire commands to and from the Java RemoteWebDriver end through the Thrift mechanism.

##Server lifecycle
One of the requirements on the client side is that tests in the ported language can be run simultaneously. This implies the Thrift server should be able to serve clients concurrently.
Among the other things, one of the problem that is solved in the porting is making sure that the server is always available when tests are running and it quits when idle.
On normal usage of the tool, the first test that needs to perform a Galen layout check will start the server. The server will be running until report is generated.
As some test implementations might want to have control of the server lifecycle, an environment variable exists that disable launching of the server by tests:
    SERVER_ALWAYS_ON=True
This assumes, Galen API service should be launched manually with the below command:
    java -jar galen-api-server.jar -r <port>

##Limitations
At the moment, only Remote Webdriver is supported.

###Assembly server jar###
Java Thrift files are not part of the repo. They are generated on the fly from the .thrift file.
In order for the server to be assembled in a jar, you need to generate thrift Java files, build and then package.
All this is automated by the script assemble_java_server.sh.
The script will eventually create a bin dir where to package the jar.

###Configure Java server log###
Log config file 'simplelogger.properties' insire resource foldercontains log configuration.
The file gets copied into classpath on assembly step.

##Galen Python API Client##
###Generate thrift file####
Pyhton Thrift files are not part of the repo. They are generated on the fly from .thrift file.
Generation of python thrift files in done via the script generate_py_thrift.sh
