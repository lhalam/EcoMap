#!/usr/bin/env bash
# Script run config builder 

PRODROOT=~/project/EcoMap/ecomap
PYSRCROOT=${PRODROOT}/src/python
CONFROOT=${PRODROOT}/etc
PYTHONPATH=$PYSRCROOT
PYTHON=$(which python)
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
STATICROOT=${PRODROOT}/www
CONFBUILDER=${PYSRCROOT}/ecomap/config_builder.py
export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE CONFBUILDER
if [ $# -eq 0 ]; then
    python $CONFBUILDER
else
    python $CONFBUILDER -v$1 
fi   
