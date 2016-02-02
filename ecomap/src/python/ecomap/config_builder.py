import os
from ConfigParser import SafeConfigParser

CONFIG_PATH = os.path.join(os.environ['CONFROOT'], '_configvars.conf')

def config_variables_parser():
    config = SafeConfigParser()
    config.readfp(open(CONFIG_PATH))
    sections = config.sections()
    template_config = {}
    for section in sections:
        template_config[section] = []
        for (key, value) in config.items(section):
            template_config[section].append(value)
    return template_config



config_read()