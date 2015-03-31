#!/bin/sh

python_folder=src/main/python
api_folder=${python_folder}/galenapi
destination_thrift_folder=${api_folder}/pythrift

thrift --gen py -o target src/main/thrift/galen_api.thrift

if [ -d "${destination_thrift_folder}" ]; then
    rm -rf ${destination_thrift_folder}
fi

mv target/gen-py/pythrift ${api_folder}/

exit 0
