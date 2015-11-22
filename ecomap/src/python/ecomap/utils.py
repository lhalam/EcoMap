import logging
import logging.config
import os

# CONF_PATH = os.path.join(os.environ['CONFROOT'], 'log.conf')
CONF_PATH = '/home/padalko/ss_projects/Lv-164.UI/ecomap/etc/log.conf'

def get_logger():
    """function for configuring default logger object
    from standard logging library
        Returns:
            configured logger object.
        Usage:
            import this method to your
            module and call it.
            then define a new logger object as usual
    """
    return logging.config.fileConfig(CONF_PATH)


class Singleton(type):
    """
    using a Singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance