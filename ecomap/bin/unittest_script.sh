#!/bin/sh
# Script for running unittest 

WAY=$PRODROOT'/unittest/src/python/ecomap'

python -m unittest discover -v $WAY
