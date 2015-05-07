#!/bin/sh

chmod +x ./distribute_galenpy.sh
./distribute_galenpy.sh -no-upload
export GALENPY_VERSION=$(python -c 'import py; print py.__version__')
pip install dist/galenpy-${GALENPY_VERSION}-py2.py3-none-any.whl
