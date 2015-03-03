#!/bin/sh

thrift --gen py -o target src/main/thrift/galen_api.thrift

rm -rf src/main/python/galenthrift

mv target/gen-py/* src/main/python/