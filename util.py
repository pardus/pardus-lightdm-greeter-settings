import configparser
import os
def list_gtk_themes():
    ret = []
    for dir in os.listdir("/usr/share/themes"):
        if os.path.isfile("/usr/share/themes/{}/gtk-3.0/gtk.css".format(dir)):
            ret.append(get_gtk_theme_name(dir)+":"+dir)
    return ret

def get_gtk_theme_name(theme):
    tcfg = configparser.RawConfigParser()
    tcfg.read("/usr/share/themes/{}/index.theme".format(theme))
    return tcfg["X-GNOME-Metatheme"]["Name"]
