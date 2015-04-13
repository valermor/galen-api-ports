
#Galen API Ports
_Galen API Ports_ is an attempt to port the [Galen Framework](http://galenframework.com "Galen's Homepage") API to languages other than Javascript and Java, which are the ones officially supported.
At the moment, only porting to Python is provided.

##License
_Galen API Ports_ is licensed under the Apache Software License 2.0 provision.

##Architecture
The idea is simple: Galen Java APIs are made available to other languages through an RPC implementation.
The RPC is based on [Apache Thrift](https://thrift.apache.org/).
A Thrift Java Server calls the Galen Java API, while clients implemented in other languages are free to expose their own API implementation.
The services Galen APIs provide can be divided into two groups:
- Hierarchical reports creation
- Layout validation based on Galen Spec language

Currently, only a Python client exists. Both server and client live in the same project.

##Json over Thrift Remote WebDriver

##Server lifecycle



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
