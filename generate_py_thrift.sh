#!/bin/sh

python_folder=py
api_folder=${python_folder}/galenpy
destination_thrift_folder=${api_folder}/pythrift

thrift --gen py -o target thrift/galen_api.thrift

if [ -d "${destination_thrift_folder}" ]; then
    rm -rf ${destination_thrift_folder}
fi

mv target/gen-py/pythrift ${api_folder}/

exit 0
