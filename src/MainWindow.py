import subprocess
from widget import *
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import util

APPDIR = os.path.dirname(os.path.abspath(__file__))


try:
    import locale
    from locale import gettext as _

    # Translation Constants:
    APPNAME = "pardus-lightdm-greeter-settings"
    TRANSLATIONS_PATH = "/usr/share/locale"
    locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
    locale.textdomain(APPNAME)
except:
    # locale load issue fix
    def _(msg):
        return msg


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=_("Pardus Lightdm Settings"))
        self.set_icon_name("pardus-lightdm-greeter-settings")

        self.set_wmclass("pardus-lightdm-greeter-settings",
                         "pardus-lightdm-greeter-settings")

        # Create Notebook
        self.notebook = Gtk.Notebook()
        scrolled_window = Gtk.ScrolledWindow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.add(box)
        scrolled_window.add(self.notebook)

        self.save_button = Gtk.Button(label=_("Save"))
        self.save_button.connect("clicked", self.save_button_event)

        self.cancel_button = Gtk.Button(label=_("Close"))
        self.cancel_button.connect("clicked", Gtk.main_quit)

        # main box
        box.pack_start(scrolled_window, True, True, 0)
        box.pack_start(box2, False, False, 3)

        # bottom box
        box2.pack_start(Gtk.Label("© TÜBİTAK BİLGEM"), False, False, 13)
        box2.pack_start(Gtk.Label(), True, True, 0)
        box2.pack_start(box3, False, False, 0)

        # button box
        box3.pack_start(Gtk.Label(), True, True, 3)
        box3.pack_start(self.save_button, False, False, 3)
        box3.pack_start(self.cancel_button, False, False, 3)

        self.settings = {}
        self.init_pages()
        self.set_size_request(600, 600)

    def add_page(self, page, label=""):
        self.notebook.append_page(page, Gtk.Label(label))

    def save_button_event(self, widget):
        dialog = Dialog(
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.NONE,
            _("Pardus Lightdm Settings"),
            _("Are you want to save current settings?"))
        dialog.add_button(_("No"), Gtk.ResponseType.NO)
        dialog.add_button(_("Yes"), Gtk.ResponseType.YES)
        if dialog.show():
            self.apply_button_event()

    def apply_button_event(self, widget=None):
        inidata = ""
        background = ""
        if "gtkwindow" in self.settings:
            if "background" in self.settings["gtkwindow"].widgets:
                background = self.settings["gtkwindow"].widgets["background"]
                background = background.get_value()
                if os.path.isfile(background) and background.startswith("/home"):
                    if os.path.isfile("/var/lib/lightdm/wallpaper"):
                        os.unlink("/var/lib/lightdm/wallpaper")
                    self.settings["gtkwindow"].widgets["background"].path = "/var/lib/lightdm/wallpaper"
        for s in self.settings:
            inidata += "[{}]\n".format(self.settings[s].name)
            dump = self.settings[s].dump()
            for key in dump:
                inidata += "{}={}\n".format(key, dump[key])
            inidata += "\n"
        autologin_user = ""
        if "lightdm" in self.settings:
            autologin_user = self.settings["lightdm"].get_value(
                "autologin-user")
        subprocess.run(["pkexec", APPDIR+"/saveconfig.py",
                       inidata, background, autologin_user],
                       check=True)

    def init_pages(self):
        pages = os.listdir("{}/data/schemas/".format(APPDIR))
        pages.sort()
        for f in pages:
            fname = f.split("-")[1].split(".")[0]
            self.settings[fname] = Settings()
            with open("{}/data/schemas/{}".format(APPDIR, f), "r") as fdata:
                jdata = json.loads(fdata.read())
                self.settings[fname].build(jdata)
                self.settings[fname].name = jdata["pardus"]["name"]
                self.add_page(self.settings[fname].get(), _(
                    jdata["pardus"]["title"]))

        for module in os.listdir(APPDIR+"/settings"):
            if not os.path.isfile("{}/settings/{}".format(APPDIR, module)) or not module.endswith(".py"):
                continue
            with open("{}/settings/{}".format(APPDIR, module), "r") as f:
                print("Loading: %s" % module)
                exec(f.read())
