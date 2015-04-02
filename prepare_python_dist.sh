#!/bin/bash

service_folder=py/galenapi/service

./update_thrift.sh

if [ ! -d "${service_folder}" ]; then
    mkdir ${service_folder}
fi

cp bin/* ${service_folder}
