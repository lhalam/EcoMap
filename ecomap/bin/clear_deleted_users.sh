#!/bin/bash
export PRODROOT=${PRODROOT:-/home/padalko/ss_projects/Lv-164.UI/ecomap}
export PYSRCROOT=${PYSRCROOT:-${PRODROOT}/src/python}
export CONFROOT=${CONFROOT:-${PRODROOT}/etc}
export PYTHONPATH=${PRODROOT}/src/python
export PYTHON=${PYTHON:-/etc/python}
export PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
export STATICROOT=${STATICROOT:-${PRODROOT}/www/}

/usr/bin/python $PYTHONPATH/ecomap/bin/clear_temporary_hash.py -t delete $*
