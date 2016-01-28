#!/bin/sh
# Script for run all unittests 

PRODROOT=${PRODROOT:-/home/roman/project/EcoMap/ecomap}
PYSRCROOT=${PYSRCROOT:-${PRODROOT}/src/python}
CONFROOT=${CONFROOT:-${PRODROOT}/etc}
PYTHONPATH=${PRODROOT}/src/python
PYTHON=${PYTHON:-/etc/python}
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
STATICROOT=${STATICROOT:-${PRODROOT}/www/}
UNITTESTPATH=${UNITTESTPATH:-${PRODROOT}/unittest/src/python/ecomap}
export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE UNITTESTPATH

python -m unittest discover -v $UNITTESTPATH
