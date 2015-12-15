#!/bin/bash
echo 'start export'

export PRODROOT=${PRODROOT:-/home/padalko/ss_projects/Lv-164.UI/ecomap}
export PYSRCROOT=${PYSRCROOT:-${PRODROOT}/src/python}
export CONFROOT=${CONFROOT:-${PRODROOT}/etc}
export PYTHONPATH=${PRODROOT}/src/python
export PYTHON=${PYTHON:-/etc/python}
export PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE:-/tmp/.python-eggs}
export STATICROOT=${STATICROOT:-${PRODROOT}/www/}

echo 'sending email'
echo date:
date
/usr/bin/python /home/padalko/ss_projects/Lv-164.UI/ecomap/src/python/ecomap/crone_admin.py

