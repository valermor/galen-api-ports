
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
