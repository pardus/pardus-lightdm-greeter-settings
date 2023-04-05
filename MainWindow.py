import gi, os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from widget import *
import util

def _(v):
    return v

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title ="Lightdm Pardus Greeter Settings")

        # Create Notebook
        self.notebook = Gtk.Notebook()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.save_button = Gtk.Button(label=_("Save"))
        self.save_button.connect("clicked",self.save_button_event)
        
        box.pack_start(self.notebook,True, True,0)
        box.pack_start(box2,False, False,0)
        box2.pack_start(Gtk.Label("TUBİTAK ULAKBIM | 2023"),True, True,0)
        box2.pack_start(self.save_button,False, False,0)
        self.add(box)
        
        self.settings = {}
        self.init_pages()


    def add_page(self,page, label=""):
        self.notebook.append_page(page, Gtk.Label(label))

    def save_button_event(self,widget):
        for s in self.settings:
            print(self.settings[s].dump())


    def init_pages(self):
        for f in os.listdir("data"):
           self.settings[f] = Settings()
           with open("data/"+f,"r") as fdata:
               jdata = json.loads(fdata.read())
               self.settings[f].build(jdata)
               self.settings[f].name = jdata["pardus"]["name"]
               self.add_page(self.settings[f].get(),_(jdata["pardus"]["title"]))
               
        # General
        self.settings["main.json"].set_data("scale",{
            "label":_("Scale"),
            "value": config.get("scale","1")
        })
        self.settings["main.json"].set_data("gtk-theme",{
            "label":_("Gtk theme"),
            "options": util.list_gtk_themes(),
            "value": config.get("gtk-theme","Adwaita")
        })
        self.settings["main.json"].set_data("font-size",{
            "label":_("Font Size"),
            "value": config.get("font-size","10")
        })
        self.settings["main.json"].set_data("dark-theme",{
            "label":_("Prefer dark theme"),
            "value": config.get("dark-theme","true")
        })
        self.settings["main.json"].set_data("blank-timeout",{
            "label":_("Black screen timeout (sec)"),
            "value": config.get("blank-timeout","300")
        })
        self.settings["main.json"].set_data("init",{
            "label":_("Initial command"),
            "value": config.get("init","")
        })
        self.settings["main.json"].set_data("prestart",{
            "label":_("Start command before login"),
             "value": config.get("prestart","")
        })
        # Lightdm
        self.settings["lightdm.json"].set_data("allow-root-login",{
            "label":_("Allow login as root"),
             "value": config.get("allow-root-login","true")
        })
        self.settings["lightdm.json"].set_data("allow-autologin",{
            "label":_("Allow autologin"),
             "value": config.get("allow-autologin","true")
        })
        self.settings["lightdm.json"].set_data("autologin-user",{
            "label":_("Autologin username"),
             "value": config.get("autologin-user","")
        })
        
        # Gtk Window
        self.settings["gtkwindow.json"].set_data("background",{
            "label":_("Background image"),
             "value": config.get("background","user"),
             "default": "user"
        })
        self.settings["gtkwindow.json"].set_data("allow-empty-password",{
            "label":_("Allow empty password"),
             "value": config.get("allow-empty-password","true")
        })
        self.settings["gtkwindow.json"].set_data("allow-empty-password",{
            "label":_("Allow emply password"),
             "value": config.get("allow-empty-password","true")
        })
        self.settings["gtkwindow.json"].set_data("password-cache",{
            "label":_("Login without enter"),
             "value": config.get("password-cache","true")
        })
        self.settings["gtkwindow.json"].set_data("username-cache",{
            "label":_("Remember last username"),
             "value": config.get("username-cache","true")
        })
        self.settings["gtkwindow.json"].set_data("logo",{
            "label":_("Custom logo"),
             "value": config.get("logo","true"),
             "default": ""
        })
