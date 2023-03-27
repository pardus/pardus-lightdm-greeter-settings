import gi, os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from widget import *

def _(v):
    return v

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title ="Lightdm Pardus Greeter Settings")

        # Create Notebook
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.settings = {}
        self.init_pages()


    def add_page(self,page, label=""):
        self.notebook.append_page(page, Gtk.Label(label))


    def init_pages(self):
        for f in os.listdir("data"):
           self.settings[f] = Settings()
           with open("data/"+f,"r") as fdata:
               jdata = json.loads(fdata.read())
               print(jdata)
               self.settings[f].build(jdata)
               self.settings[f].name = jdata["pardus"]["name"]
               self.add_page(self.settings[f].get(),jdata["pardus"]["title"])
               
        # main page
        self.settings["main.json"].set_data("scale",{"label":_("Scale")})
        self.settings["main.json"].set_data("gtk-theme",{"label":_("Gtk theme"),"options": os.listdir("/usr/share/themes")})
        self.settings["main.json"].set_data("dark-theme",{"label":_("Prefer dark theme")})
        self.settings["main.json"].set_data("blank-timeout",{"label":_("Black screen before wait time")})
        self.settings["main.json"].set_data("init",{"label":_("Initial command")})
        self.settings["main.json"].set_data("prestart",{"label":_("Start command before login")})
