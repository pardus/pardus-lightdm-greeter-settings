import configparser
import os
import sys

if os.path.isdir("/usr/share/pardus/pardus-lightdm-greeter/module"):
    sys.path.insert(0, "/usr/share/pardus/pardus-lightdm-greeter/module")

import monitor
m = monitor.monitor_class()


def list_monitors():
    ret = []
    for mon in m.get_monitors():
        ret.append(mon+":"+mon)
    return ret


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
