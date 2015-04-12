#Galen API Ports
_Galen API Ports_ is an attempt to port the [Galen Framework](http://galenframework.com "Galen's Homepage") API to languages other than Javascript and Java, which are officially supported.
At the moment, only Python is supported.

#License
_Galen API Ports_ is licensed under the Apache Software License provision.


#Architecture
The architecture is based on [Apache Thrift](https://thrift.apache.org/).
In a nutshell, the Java Galen API is accessed by a Thrift Server which makes it available to clients implemented in othe languange.
Two APIs from Galen Framework are currently available:
- Hierarchical reports API
- Layout validation based on Galen Spec language


##Galen API Server##
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
