#!/usr/bin/env bash
# Script run config builder

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PRODROOT=${SCRIPT_DIR%/*}
echo "Product directory: $PRODROOT"
PYSRCROOT=${PRODROOT}/src/python
CONFROOT=${PRODROOT}/etc
PYTHONPATH=$PYSRCROOT
PYTHON=${PYTHON:-/etc/python}
PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
export PRODROOT PYSRCROOT PYTHONPATH CONFROOT STATICROOT PYTHON_EGG_CACHE

python ${PYSRCROOT}/ecomap/config_builder.py $@
