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
        scrolled_window = Gtk.ScrolledWindow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.add(box)
        scrolled_window.add(self.notebook)
        
        self.save_button = Gtk.Button(label=_("Save"))
        self.save_button.connect("clicked",self.save_button_event)

        self.cancel_button = Gtk.Button(label=_("Cancel"))
        self.cancel_button.connect("clicked",Gtk.main_quit)
        
        # main box
        box.pack_start(scrolled_window,True, True,0)
        box.pack_start(box2,False, False,3)

        # bottom box
        box2.pack_start(Gtk.Label("TUBİTAK ULAKBIM | 2023"),False, False,13)
        box2.pack_start(Gtk.Label(),True, True,0)
        box2.pack_start(box3,False, False,0)

        # button box
        box3.pack_start(Gtk.Label(),True, True,3)
        box3.pack_start(self.cancel_button,False, False,3)
        box3.pack_start(self.save_button,False, False,3)

        
        self.settings = {}
        self.init_pages()
        self.set_size_request(600,600)


    def add_page(self,page, label=""):
        self.notebook.append_page(page, Gtk.Label(label))

    def save_button_event(self,widget):
        inidata = ""
        for s in self.settings:
            inidata += "[{}]\n".format(self.settings[s].name)
            dump = self.settings[s].dump()
            for key in dump:
                inidata += "{}={}\n".format(key,dump[key])
            inidata += "\n"
        print(inidata)


    def init_pages(self):
        for f in os.listdir("data"):
           self.settings[f] = Settings()
           with open("data/"+f,"r") as fdata:
               jdata = json.loads(fdata.read())
               self.settings[f].build(jdata)
               self.settings[f].name = jdata["pardus"]["name"]
               self.add_page(self.settings[f].get(),_(jdata["pardus"]["title"]))

        for module in os.listdir("settings"):
            if not os.path.isfile("settings/{}".format(module)) or not module.endswith(".py"):
                continue
            with open("settings/{}".format(module),"r") as f:
                print("Loading: %s" % module)
                exec(f.read())

