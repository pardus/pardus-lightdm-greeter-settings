import configparser
import os
try:
    cfgs = ["/etc/pardus/greeter.conf", "/etc/lightdm/lightdm.conf"]
    for fdir in ["/usr/share/lightdm/lightdm.conf.d/", "/etc/pardus/greeter.conf.d/"]:
        if os.path.isdir(fdir):
            for cdir in os.listdir(fdir):
                cfgs.append(fdir+cdir)

    config = configparser.RawConfigParser()
    config.read(cfgs)
except:
    print("Failed to read config. Using defaults")
    config = []

# print({section: dict(config[section]) for section in config.sections()})


def config_write(path):
    with open(path, 'w') as configfile:
        config.write(configfile)


def get(variable, default=None, section="pardus"):
    if section not in config:
        return default
    if variable not in config[section]:
        print(variable)
        return default
    ret = config[section][variable]
    return str(ret)


def config_set(name, value, section="pardus"):
    if section not in config:
        config[section] = {}
    config[section][name] = value
