#!/bin/bash

service_folder=src/main/python/galenapi/service

./update_thrift.sh

if [ ! -d "${service_folder}" ]; then
    mkdir ${service_folder}
fi

cp bin/* ${service_folder}
