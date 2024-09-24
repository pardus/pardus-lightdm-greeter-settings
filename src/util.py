import configparser
import os, sys

if os.path.isdir("/usr/share/pardus/pardus-lightdm-greeter/module"):
    sys.path.insert("/usr/share/pardus/pardus-lightdm-greeter/module", 0)

import monitor
m = monitor.monitor_class()
def list_monitors():
    return m.get_drm_monitors()

def list_gtk_themes():
    ret = []
    for dir in os.listdir("/usr/share/themes"):
        if os.path.isfile("/usr/share/themes/{}/gtk-3.0/gtk.css".format(dir)):
            ret.append(dir+":"+dir)
    return ret

def list_icon_themes():
    ret = []
    for dir in os.listdir("/usr/share/icons"):
        if os.path.isfile("/usr/share/icons/{}/index.theme".format(dir)):
            ret.append(dir+":"+dir)
    return ret


def readfile(path):
    f = open(path, "r")
    ret = f.read()
    f.close()
    del (f)
    return ret

