import logging
import sys
import os

os.environ['PRODROOT'] = "/home/andjey_/lv-164/Lv-164.UI/ecomap"
os.environ['PYSRCROOT'] = "/home/andjey_/lv-164/Lv-164.UI/ecomap/src/python"
os.environ['CONFROOT'] = "/home/andjey_/lv-164/Lv-164.UI/ecomap/etc"
os.environ['PYTHONPATH'] = "/home/andjey_/lv-164/Lv-164.UI/ecomap/src/python"


# sys.path.insert (0,'/home/andjey_/lv-164/Lv-164.UI/ecomap/src/python/ecomap')
# sys.path.insert (1,'/home/andjey_/lv-164/Lv-164.UI/ecomap/src/python/')

# os.chdir('/home/andjey_/lv-164/Lv-164.UI/ecomap/src/python/')

#from ecomap.utils import get_logger
#get_logger()

from ecomap.app import ecomap as application

application.secret_key = "topsecret!"
