# !/usr/bin/env bash
# Script run config builder 

PRODROOT=~/home/workspace/test_ecomap/ecomap
PYSRCROOT=${PRODROOT}/src/python
CONFROOT=${PRODROOT}/etc
PYTHONPATH=$PYSRCROOT
PYTHON=${PYTHON:-/etc/python}
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
LOGLEVEL=${1:-1}
export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE

python ${PYSRCROOT}/ecomap/config_builder.py -v$LOGLEVEL
