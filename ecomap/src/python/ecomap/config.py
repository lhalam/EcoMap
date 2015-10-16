"""
Module which contains Config class. This class is singleton.
It exists to parse *.conf files and return dictionary,
which contains configuration from those files. Every 15 minutes
it returns new dictionary which contains updated configs.
"""
from ConfigParser import SafeConfigParser
import logging
import time
import unittest

logging.basicConfig(level=logging.INFO)
REFRESH_TIME = 900                               # 15 minutes
PASSWORD = 'password'


class Singleton(type):
    """
    Metaclass for make Config class singleton.
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Config(object):

    """
    Singleton class which returns object which have method
    to parse config file every 15 minutes.
    :param path: name of file
    """
    __metaclass__ = Singleton

    def __init__(self, path):
        self.config = {}                         # dictionary, contains configs
        self.update_time = 0                     # time of living
        self.path = path                         # path to file (temporary)
        self.logger = logging.getLogger('exapmle')
        self.logger.debug('Initialized instance at: %s', time.time())

    def get_config(self):                        # method which checks if we
        """
        Checks if it is needed to reload configs.
        Before calling parsing functian checks if
        elapsed 15 minutes after last update.
        returns: dictionary
        """
        self.logger.debug('Check if need to update at %s', time.time())
        if self.update_time < time.time():       # need to update configs
            self.config = {}                     # nullify configs dictionary
            self.update_time = time.time() + REFRESH_TIME  # set time to update
            self._parse_confs()                  # parse config file
        return self.config

    def _parse_confs(self):
        """
        Parses config file and returns dictionary.
        """
        self.logger.debug('Parsed ecomap.conf at %s', (time.time()))
        config = SafeConfigParser()              # create config object
        config.readfp(open(self.path))           # read file
        sections = config.sections()             # get sections
        for section in sections:                 # for each section
            for (key, value) in config.items(section):   # for each key/value
                if value and key != PASSWORD:
                    try:
                        value = eval(value)
                    except NameError:
                        pass
                self.config[section + '.' + key] = value


if __name__ == '__main__':

    FIRST = Config('../../../etc/ecomap.conf')
    SECOND = Config('../../../etc/ecomap.conf')

    class Test(unittest.TestCase):
        """
        Test class which inherits unittest.TestCase and
        provides 3 tests for Config class.
        """
        def test_sameinstances(self):
            """
            Check if different calls returns same instance.
            """
            self.assertEquals(FIRST, SECOND)

        def test_config(self):
            """
            Check if different calls return same configs.
            """
            self.assertEquals(FIRST.get_config(), SECOND.get_config())

        def test_updatetime(self):
            """
            Check if different calls have same update_time
            """
            self.assertEquals(FIRST.update_time, SECOND.update_time)

    unittest.main()

# ************* Module config
# W: 23,12: Attribute '_instance' defined outside __init__ (attribute-defined-outside-init)
# R: 28, 0: Too few public methods (1/2) (too-few-public-methods)
# R: 79, 4: Too many public methods (48/20) (too-many-public-methods)


# Report
# ======
# 52 statements analysed.

# Statistics by type
# ------------------

# +---------+-------+-----------+-----------+------------+---------+
# |type     |number |old number |difference |%documented |%badname |
# +=========+=======+===========+===========+============+=========+
# |module   |1      |1          |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |class    |3      |3          |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |method   |7      |7          |=          |100.00      |0.00     |
# +---------+-------+-----------+-----------+------------+---------+
# |function |0      |0          |=          |0           |0        |
# +---------+-------+-----------+-----------+------------+---------+



# Raw metrics
# -----------

# +----------+-------+------+---------+-----------+
# |type      |number |%     |previous |difference |
# +==========+=======+======+=========+===========+
# |code      |52     |52.53 |52       |=          |
# +----------+-------+------+---------+-----------+
# |docstring |34     |34.34 |34       |=          |
# +----------+-------+------+---------+-----------+
# |comment   |0      |0.00  |0        |=          |
# +----------+-------+------+---------+-----------+
# |empty     |13     |13.13 |13       |=          |
# +----------+-------+------+---------+-----------+



# Messages by category
# --------------------

# +-----------+-------+---------+-----------+
# |type       |number |previous |difference |
# +===========+=======+=========+===========+
# |convention |0      |0        |=          |
# +-----------+-------+---------+-----------+
# |refactor   |2      |2        |=          |
# +-----------+-------+---------+-----------+
# |warning    |1      |1        |=          |
# +-----------+-------+---------+-----------+
# |error      |0      |0        |=          |
# +-----------+-------+---------+-----------+



# Messages
# --------

# +-------------------------------+------------+
# |message id                     |occurrences |
# +===============================+============+
# |too-many-public-methods        |1           |
# +-------------------------------+------------+
# |too-few-public-methods         |1           |
# +-------------------------------+------------+
# |attribute-defined-outside-init |1           |
# +-------------------------------+------------+



# Global evaluation
# -----------------
# Your code has been rated at 9.42/10 (previous run: 9.42/10, +0.00)

# Duplication
# -----------

# +-------------------------+------+---------+-----------+
# |                         |now   |previous |difference |
# +=========================+======+=========+===========+
# |nb duplicated lines      |0     |0        |=          |
# +-------------------------+------+---------+-----------+
# |percent duplicated lines |0.000 |0.000    |=          |
# +-------------------------+------+---------+-----------+



