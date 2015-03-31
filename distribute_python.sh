#!/bin/bash -x

python_project_root=src/main/python
project_root=${PWD##*/}

echo "packaging python libs"
./prepare_python_dist.sh

echo "creating a source distribution"

if [ -d "${python_project_root}/build" ]; then
    rm -rf ${python_project_root}/build
fi

if [ -d "${python_project_root}/dist" ]; then
    rm -rf ${python_project_root}/dist
fi

if [ -d "${python_project_root}/galenapi.egg-info" ]; then
    rm -rf ${python_project_root}/galenapi.egg-info
fi
cd ${python_project_root}

python setup.py sdist

echo "creating wheel"

python setup.py bdist_wheel
