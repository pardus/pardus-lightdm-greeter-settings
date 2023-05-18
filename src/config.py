import configparser
import os
try:
    cfgs = ["/etc/pardus/greeter.conf","/etc/lightdm/lightdm.conf"]
    for fdir in ["/usr/share/lightdm/lightdm.conf.d/","/etc/pardus/greeter.conf.d"]:
        if os.path.isdir(fdir):
            for cdir in os.listdir(fdir):
                cfgs.append(fdir+cdir)

    config = configparser.RawConfigParser()
    config.read(cfgs)
except:
    print("Failed to read config. Using defaults")
    config = []

print({section: dict(config[section]) for section in config.sections()})

def get(variable, default=None, section="pardus"):
    if section not in config:
        return default
    if variable not in config[section]:
        return default
    ret = config[section][variable]
    return str(ret)