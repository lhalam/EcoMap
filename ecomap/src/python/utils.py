from logging import config
import os


CONF_PATH = os.path.join(os.environ['CONFROOT'], 'log.conf')


def get_logger():

    """create a regular logger as usual.
        :return:  configured logger object.
        usage: import this method to your
        module and call it.
    """

    return config.fileConfig(CONF_PATH)


class Singleton(type):
    """
    using a singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
