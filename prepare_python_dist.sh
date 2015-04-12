#!/bin/bash

service_folder=py/galenpy/service

echo "assembling Java server"
./assemble_java_server.sh

echo "generating Python Thrift files"
./generate_py_thrift.sh

if [ ! -d "${service_folder}" ]; then
    mkdir ${service_folder}
fi

cp bin/* ${service_folder}
