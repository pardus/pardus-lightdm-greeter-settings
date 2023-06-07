import configparser
import os


def list_gtk_themes():
    ret = []
    for dir in os.listdir("/usr/share/themes"):
        if os.path.isfile("/usr/share/themes/{}/gtk-3.0/gtk.css".format(dir)):
            tname = get_gtk_theme_name(dir)
            if tname:
                ret.append(tname+":"+dir)
    return ret

lang=os.environ["LANG"].split(".")[0].split("_")[0]
def get_gtk_theme_name(theme):
    tcfg = configparser.RawConfigParser()
    tcfg.read("/usr/share/themes/{}/index.theme".format(theme))
    if "X-GNOME-Metatheme" in tcfg:
        if "Name[{}]".format(lang) in tcfg["X-GNOME-Metatheme"]:
            return tcfg["X-GNOME-Metatheme"]["Name[{}]".format(lang)]
        elif "Name" in tcfg["X-GNOME-Metatheme"]:
            return tcfg["X-GNOME-Metatheme"]["Name"]
        return theme
    return theme


def list_icon_themes():
    ret = []
    for dir in os.listdir("/usr/share/icons"):
        if os.path.isfile("/usr/share/icons/{}/index.theme".format(dir)):
            tname = get_icon_theme_name(dir)
            if tname:
                ret.append(tname+":"+dir)
    return ret


def readfile(path):
    f = open(path, "r")
    ret = f.read()
    f.close()
    del (f)
    return ret


def get_icon_theme_name(theme):
    tcfg = configparser.RawConfigParser()
    for line in readfile("/usr/share/icons/{}/index.theme".format(theme)):
        if line.startswith("Name="):
            return line[len("Name="):]
    return theme
