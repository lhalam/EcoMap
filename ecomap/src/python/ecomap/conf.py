import ConfigParser
from threading import Timer


class RepeatedTimer(object):

    """This is additional support class
    which stands as wrapper for repeating
    actions in excact intervals"""

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        """This functions runs the action and
        calls start() to repeat the action"""
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """This function will call run() function
        in previously passed interval time."""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """This function stop repeating of the action."""
        self._timer.cancel()
        self.is_running = False


class Config(object):

    """This is singleton class, which collects
    configurations from file ecomap/etc/config.conf
    every 15 minutes(by default)"""

    obj = None

    def __new__(cls, file_path, interval=900):
        if cls.obj is None:
            cls.obj = super(Config, cls).__new__(cls)
            cls.obj.config = ConfigParser.SafeConfigParser()
            cls.obj.file_path = file_path
            cls.obj.conf_dict = {}
            cls.obj.interval = interval
        return cls.obj

    def get_dict(self):
        """This function read configs from
        file and parses those configs into
        dictionary, which will be returned."""
        self.config.read(self.file_path)
        self.conf_dict = {}
        sections = self.config.sections()
        for section in sections:
            options = self.config.options(section)
            for option in options:
                try:
                    # what if here will be 0 or 1???
                    value = self.config.getboolean(section, option)
                except ValueError:
                    try:
                        if '.' in self.config.get(section, option):
                            value = self.config.getfloat(section, option)
                        else:
                            value = self.config.getint(section, option)
                    except ValueError:
                        value = self.config.get(section, option)
                finally:
                    self.conf_dict[section + '.' + option] = value
        return self.conf_dict

    def __refresh_dict(self):
        """This function simply calls
        get_dict() to refresh the dict."""
        self.conf_dict = self.get_dict()
        print self.conf_dict

    def start_tracking(self):
        """This function starts refreshing
        configs every 15 minutes(by default).
        It will end after user interruption(Ctrl^C)"""
        timer = RepeatedTimer(self.interval, self.__refresh_dict)
        try:
            timer.start()
        except:
            timer.stop()


if __name__ == '__main__':
    conf = Config('../../../etc/ecomap.conf', 3)
    conf.start_tracking()
    print conf.get_dict()
