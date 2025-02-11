import config
import json
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class settings_object(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.hidden = False


class object_onoff(settings_object):
    def __init__(self):
        super().__init__()
        self.switch = Gtk.Switch()
        self.image = Gtk.Image()
        self.label = Gtk.Label()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(), True, True, 3)
        self.pack_start(self.switch, False, False, 3)
        self.show_all()
        self.switch.connect("state-set", self.__state_event)
        self.state_event = None

    def __state_event(self, widget, state):
        if self.state_event:
            self.state_event(widget, state)

    def set_data(self, data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"], 0)
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
        self.pack_start(Gtk.Label(), True, True, 3)
        self.pack_start(self.entry, False, False, 3)
        self.show_all()

    def set_data(self, data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"], 0)
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
        self.reset = Gtk.Button()
        self.default_button_label = ""
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(), True, True, 3)
        self.pack_start(self.reset, False, False, 3)
        self.pack_start(self.button, False, False, 3)
        self.button.connect("clicked", self.select_file)
        self.default = ""
        self.path = None
        self.reset.set_image(
            Gtk.Image.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON))
        self.reset.set_relief(Gtk.ReliefStyle.NONE)
        self.reset.connect("clicked", self.reset_value)

    def select_file(self, widget):
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
        data = {}
        data["value"] = self.default
        if response == Gtk.ResponseType.OK:
            data["value"] = dialog.get_filename()

        self.set_data(data)
        dialog.destroy()

    def set_data(self, data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "button_label" in data:
            self.default_button_label = data["button_label"]
        if "image" in data:
            self.image.set_from_icon_name(data["image"], 0)
        if "default" in data:
            self.default = data["default"]
        if "value" in data:
            self.path = data["value"]
            if self.default != self.path:
                self.button.set_label(os.path.basename(self.path))
            else:
                self.button.set_label(self.default_button_label)
        print(self.path, self.default)

    def reset_value(self, widget=None):
        self.button.set_label(self.default_button_label)
        data = {}
        data["value"] = self.default
        self.set_data(data)

    def get_value(self):
        if self.path:
            return self.path
        return self.default


class object_number(settings_object):
    def __init__(self):
        super().__init__()
        self.spinbutton = Gtk.SpinButton()
        self.label = Gtk.Label()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(), True, True, 3)
        self.pack_start(self.spinbutton, False, False, 3)
        self.spinbutton.set_increments(1, 1)
        self.spinbutton.set_digits(0)
        self.show_all()
        self._digit = 0

    def set_data(self, data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"], 0)
        self._digit = 0
        if "digit" in data:
            self._digit = float(data["digit"])
            self.spinbutton.set_increments(1/10**self._digit, 1)
            self.spinbutton.set_digits(self._digit)
        if "min" in data and "max" in data:
            self.spinbutton.set_range(float(data["min"]), float(data["max"]))
        if "value" in data:
            self.spinbutton.set_value(float(data["value"]))

    def get_value(self):
        if self._digit == 0:
            return int(self.spinbutton.get_value())
        else:
            return self.spinbutton.get_value()


class object_selection(settings_object):
    def __init__(self):
        super().__init__()
        self.label = Gtk.Label()
        self.combo = Gtk.ComboBox()
        self.image = Gtk.Image()
        self.pack_start(self.image, False, False, 3)
        self.pack_start(self.label, False, False, 3)
        self.pack_start(Gtk.Label(), True, True, 3)
        self.pack_start(self.combo, False, False, 3)
        self.show_all()
        self.__opts = None
        cell_renderer = Gtk.CellRendererText()
        self.combo.pack_start(cell_renderer, True)
        self.combo.add_attribute(cell_renderer, "text", 0)

    def set_data(self, data):
        if "label" in data:
            self.label.set_text(data["label"])
        if "image" in data:
            self.image.set_from_icon_name(data["image"], 0)
        if "options" in data:
            self.__opts = data["options"]
            store = Gtk.ListStore(str, str)
            for opt in data["options"]:
                if ":" in opt:
                    store.append([opt.split(":")[0], opt.split(":")[1]])
                else:
                    store.append([opt, opt])
            self.combo.set_model(store)
        if "value" in data:
            if self.__opts:
                value = data["value"]
                i = 0
                if ":" in value:
                    if value in self.__opts:
                        i = self.__opts.index(value)
                else:
                    for item in self.__opts:
                        if item.startswith(value+":") or item.endswith(value+":"):
                            break
                        i += 1
                self.combo.set_active(i)
            print(data, self.__opts)

    def get_value(self):
        tree_iter = self.combo.get_active_iter()
        if tree_iter is not None:
            model = self.combo.get_model()
            return model[tree_iter][-1]
        return ""


class Dialog(Gtk.MessageDialog):
    def __init__(self, style, buttons, title, text, text2=None, parent=None):
        Gtk.MessageDialog.__init__(self, parent, 0, style, buttons)
        self.set_position(Gtk.WindowPosition.CENTER)
        # self.set_icon_from_file("./branding/icon.svg")
        self.set_title(title)
        if text:
            self.set_property("text", text)
            self.desc = text[:30] + ' ...' if len(text) > 30 else text
        if text2:
            self.set_property("secondary_text", text2)
        if parent:
            self.set_transient_for(parent)
            self.set_modal(True)

    def show(self):
        try:
            response = self.run()
            if response in (Gtk.ResponseType.YES, Gtk.ResponseType.APPLY,
                            Gtk.ResponseType.OK, Gtk.ResponseType.ACCEPT):
                return True
            else:
                return False
        finally:
            self.destroy()


class Settings:
    def __init__(self):
        self.ONOFF = "onoff"
        self.COMBO = "combo"
        self.ENTRY = "entry"
        self.NUMBER = "number"
        self.FILEPICKER = "filepicker"
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
            if not self.widgets[w].hidden:
                ret[w] = self.widgets[w].get_value()
        return ret

    def get_value(self, name):
        if name in self.widgets:
            return self.widgets[name].get_value()
        return None

    def set_data(self, name, data, hidden=False):
        if name in self.widgets:
            self.widgets[name].set_data(data)
            self.widgets[name].hidden = hidden

    def build(self, json_data):
        for widget in json_data:
            if widget == "pardus":
                continue
            self.add_option(
                widget, json_data[widget]["type"], json_data[widget])
