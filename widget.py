import gi, os
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
import json
import config

def _(v):
    return v

class settings_object(Gtk.Box):
    def __init__(self):
        super().__init__()


class object_onoff(settings_object):
    def __init__(self):
        super().__init__()
        self.switch = Gtk.Switch()
        self.image = Gtk.Image()
        self.label = Gtk.Label()
        self.pack_start(self.image,False, False, 3)
        self.pack_start(self.label,False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.switch,False, False, 3)
        self.show_all()

    def set_data(self,data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "value" in data:
            self.switch.set_state(data["value"].lower() == "true")

    def get_value(self):
        return self.switch.get_state()

class object_entry(settings_object):
    def __init__(self):
        super().__init__()
        self.entry = Gtk.Entry()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.entry, False, False, 3)
        self.show_all()

    def set_data(self, data):
        if "label" in data:
           self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "value" in data:
           self.entry.set_text(data["value"])

    def get_value(self):
        return self.entry.get_text()

class object_filepicker(settings_object):
    def __init__(self):
        super().__init__()
        self.entry = Gtk.Entry()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.button = Gtk.Button()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.button, False, False, 3)
        self.button.connect("clicked",self.select_file)
        self.button.set_label(_("Default"))
        self.default="default"

    def select_file(self,widget):
        dialog = Gtk.FileChooserDialog(
            title=self.label.get_text(), parent=None, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        response = dialog.run()
        self.path = None
        if response == Gtk.ResponseType.OK:
            self.path = dialog.get_filename()
        if self.path:
            self.button.set_label(os.path.basename(self.path))
        else:
            self.button.set_label(_("Default"))
            self.path = self.default
            
        dialog.destroy()

    def set_data(self, data):
        if "label" in data:
           self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "default" in data:
            self.default = data["default"]


    def get_value(self):
        return self.path

class object_number(settings_object):
    def __init__(self):
        super().__init__()
        self.spinbutton = Gtk.SpinButton()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.spinbutton, False, False, 3)
        self.show_all()

    def set_data(self, data):
        if "label" in data:
           self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "min" in data and "max" in data:
           step = 1
           if "step" in data:
              step = int(data["step"])
           self.spinbutton.set_increments(step, step)
           self.spinbutton.set_range(int(data["min"]), int(data["max"]))
        if "value" in data:
            self.spinbutton.set_value(int(data["value"]))

    def get_value(self):
        return self.spinbutton.get_value()

class object_selection(settings_object):
    def __init__(self):
        super().__init__()
        self.label = Gtk.Label()
        self.combo = Gtk.ComboBox()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(),True, True, 3)
        self.pack_start(self.combo, False, False, 3)
        self.show_all()
        self.__opts = None
        cell_renderer = Gtk.CellRendererText()
        self.combo.pack_start(cell_renderer,True)
        self.combo.add_attribute(cell_renderer, "text", 0)
        self.combo.connect("changed", self.on_combobox_changed)

    def on_combobox_changed(self, combobox):
        treeiter = combobox.get_active_iter()
        model = combobox.get_model()

        print("ComboBox selected item: %s" % (model[treeiter][1]))

    def set_data(self,data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"],0)
        if "options" in data:
            self.__opts = data["options"]
            store = Gtk.ListStore(str,str)
            for opt in data["options"]:
                if ":" in opt:
                    store.append([opt.split(":")[0],opt.split(":")[1]])
                else:
                    store.append([opt, opt])
            self.combo.set_model(store)
        if "value" in data:
            if self.__opts:
                value = data["value"]
                if ":" not in value:
                    value = value+":"+value
                if value in self.__opts:
                    i = self.__opts.index(value)
                    self.combo.set_active(i)

    def get_value(self):
        tree_iter = self.combo.get_active_iter()
        if tree_iter is not None:
            model = self.combo.get_model()
            return model[tree_iter][0]
        return ""


class Settings:
    def __init__(self):
        self.ONOFF="onoff"
        self.COMBO="combo"
        self.ENTRY="entry"
        self.NUMBER="number"
        self.FILEPICKER="filepicker"
        self.widgets = {}
        self.name = ""

    def get(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for w in self.widgets:
            box.pack_start(self.widgets[w], False, False, 5)
        box.show()
        return box

    def add_option(self, name="", type="", data=None):
        if type == self.ONOFF:
            obj = object_onoff()
        if type == self.COMBO:
            obj = object_selection()
        if type == self.ENTRY:
            obj = object_entry()
        if type == self.NUMBER:
            obj = object_number()
        if type == self.FILEPICKER:
            obj = object_filepicker()
        self.widgets[name] = obj
        obj.set_data(data)

    def dump(self):
        ret = {}
        for w in self.widgets:
            ret[w] = self.widgets[w].get_value()
        return ret

    def set_data(self,name,data):
        if name in self.widgets:
            self.widgets[name].set_data(data)

    def build(self,json_data):
        for widget in json_data:
            if widget == "pardus":
                continue
            self.add_option(widget, json_data[widget]["type"],json_data[widget])

