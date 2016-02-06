#!/usr/bin/env bash
# Script for run all unittests 

PRODROOT=~/home/workspace/test_ecomap/ecomap
PYSRCROOT=${PRODROOT}/src/python
CONFROOT=${PRODROOT}/etc
PYTHONPATH=$PYSRCROOT
PYTHON=$(which python)
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
STATICROOT=${PRODROOT}/www
UNITTESTPATH=${PRODROOT}/unittest/src/python/ecomap
export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE UNITTESTPATH

python -m unittest discover -v $UNITTESTPATH
