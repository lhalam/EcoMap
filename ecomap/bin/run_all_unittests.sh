#!/usr/bin/env bash
# Script for run all unittests 

PRODROOT=~/home/workspace/test_ecomap/ecomap
PYSRCROOT=${PRODROOT}/src/python
CONFROOT=${PRODROOT}/etc
PYTHONPATH=$PYSRCROOT
PYTHON=${PYTHON:-/etc/python}
STATICROOT=${STATICROOT:-${PRODROOT}/www/}
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}

export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE

python -m unittest discover -v ${PRODROOT}/unittest/src/python/ecomap
