#!/bin/sh

python_folder=src/main/python
destination_thrift_folder=${python_folder}/galenthrift

thrift --gen py -o target src/main/thrift/galen_api.thrift

if [ "$(ls -A ${destination_thrift_folder})" ]; then
    rm -rf ${destination_thrift_folder}
fi

mv target/gen-py/* ${python_folder}/

exit 1