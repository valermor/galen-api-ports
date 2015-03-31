#!/bin/bash

echo "assembling Java server"
./assemble_java_server.sh


echo "generating Python Thrift files"
./generate_py_thrift.sh
