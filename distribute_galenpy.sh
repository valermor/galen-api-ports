#!/bin/bash

echo "packaging python libs"
./prepare_python_dist.sh

echo "creating a source distribution"

if [ -d "build" ]; then
    rm -rf build
fi

if [ -d "dist" ]; then
    rm -rf dist
fi

if [ -d "galenapi.egg-info" ]; then
    rm -rf galenapi.egg-info
fi

if [ "$1" == "-no-upload" ]
then
    echo "creating source distribution"
    python setup.py sdist
    echo "creating wheel distribution"
    python setup.py bdist_wheel
else
    echo "uploading source distribution"
    python setup.py sdist upload -r pypi

    echo "uploading wheel distribution"
    python setup.py bdist_wheel upload -r pypi
fi


