#!/bin/bash

# Prepare Python project for distribution:
# 1 - Assemble Java Server into jar
# 2 - Copy jar to folder inside Python project for distribution
# 3 - Generate Python Thrift files.

service_folder=py/galenpy/service
python_folder=py
api_folder=${python_folder}/galenpy
destination_thrift_folder=${api_folder}/pythrift

echo "assembling Java server to ${service_folder}"
./assemble_java_server.sh

if [ ! -d "${service_folder}" ]; then
    mkdir ${service_folder}
fi

cp bin/* ${service_folder}

echo "generating Python Thrift files"
thrift --gen py -o target thrift/galen_api.thrift

if [ -d "${destination_thrift_folder}" ]; then
    rm -rf ${destination_thrift_folder}
fi

mv target/gen-py/pythrift ${api_folder}/
